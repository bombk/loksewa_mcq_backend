from datetime import timedelta

from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import (
    Category, PaperCategory, Question, QuestionPaper, UserProgress,
    MockTest, MockTestQuestion,
)
from .serializers import (
    CategorySerializer, PaperCategorySerializer, QuestionPaperSerializer,
    QuestionSerializer, UserProgressSerializer, MockTestSerializer,
)


class QuestionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = None

    def list(self, request, *args, **kwargs):
        cache_key = 'homepage:categories:v1'
        data = cache.get(cache_key)
        if data is None:
            queryset = self.filter_queryset(self.get_queryset())
            data = self.get_serializer(queryset, many=True).data
            cache.set(cache_key, data, 600)
        return Response(data)


class PaperCategoryViewSet(viewsets.ModelViewSet):
    queryset = PaperCategory.objects.all()
    serializer_class = PaperCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = None


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    pagination_class = QuestionPagination

    def get_queryset(self):
        queryset = Question.objects.select_related(
            'category', 'sub_category'
        ).prefetch_related('options').order_by('id')

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category) if category.isdigit() else queryset.filter(category__slug=category)

        sub_category = self.request.query_params.get('sub_category')
        if sub_category:
            queryset = queryset.filter(sub_category_id=sub_category) if sub_category.isdigit() else queryset.filter(sub_category__slug=sub_category)

        return queryset


class QuestionPaperViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionPaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = QuestionPaper.objects.filter(is_verified=True).select_related('category')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category) if category.isdigit() else queryset.filter(category__slug=category)
        return queryset.order_by('-uploaded_at')


class UserProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProgressSerializer

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).select_related('question')

    def perform_create(self, serializer):
        UserProgress.objects.update_or_create(
            user=self.request.user,
            question=serializer.validated_data['question'],
            defaults={'is_correct': serializer.validated_data['is_correct']},
        )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        progress = UserProgress.objects.filter(user=request.user)
        total_attempts = progress.count()
        correct_attempts = progress.filter(is_correct=True).count()
        category_stats = progress.values('question__category__name').annotate(
            total=Count('id'), correct=Count('id', filter=Q(is_correct=True)),
        )
        today = timezone.localdate()
        activity_log = []
        for offset in range(6, -1, -1):
            date = today - timedelta(days=offset)
            activity_log.append({'date': date.isoformat(), 'count': progress.filter(answered_at__date=date).count()})
        return Response({'total_attempts': total_attempts, 'correct_attempts': correct_attempts,
                         'category_stats': list(category_stats), 'activity_log': activity_log})

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def leaderboard(self, request):
        from django.contrib.auth.models import User
        cache_key = 'leaderboard:top5:v1'
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)
        top_users = User.objects.annotate(
            score=Count('progress', filter=Q(progress__is_correct=True))
        ).filter(score__gt=0).order_by('-score', 'username')[:5]
        data = [{'username': user.username, 'score': user.score,
                 'profile_photo': (request.build_absolute_uri(user.profile.profile_photo.url)
                                   if hasattr(user, 'profile') and user.profile.profile_photo else None),
                 'color_seed': len(user.username)} for user in top_users]
        cache.set(cache_key, data, 60)
        return Response(data)


class MockTestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MockTestSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return MockTest.objects.filter(user=self.request.user).prefetch_related(
            'test_questions__question__options',
            'test_questions__question__category',
            'test_questions__question__sub_category',
            'test_questions__selected_option',
        ).order_by('-started_at')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        category_ids = request.data.get('categories', [])
        if isinstance(category_ids, str):
            category_ids = [x.strip() for x in category_ids.split(',') if x.strip()]

        questions = Question.objects.select_related('category', 'sub_category').prefetch_related('options')
        if category_ids:
            questions = questions.filter(category_id__in=category_ids)

        # Select the requested test size without calculating the total question count.
        requested_size = min(int(request.data.get('total_questions', 100)), 100)
        question_list = list(questions.order_by('?')[:requested_size])
        if len(question_list) < requested_size:
            return Response({'detail': f'Only {len(question_list)} questions are available for the selected categories.'}, status=400)

        duration = min(int(request.data.get('duration_minutes', 60)), 180)
        title = request.data.get('title', 'Mock Test')
        test = MockTest.objects.create(user=request.user, title=title,
                                       duration_minutes=duration,
                                       total_questions=requested_size)
        MockTestQuestion.objects.bulk_create([
            MockTestQuestion(mock_test=test, question=question, question_order=index)
            for index, question in enumerate(question_list, start=1)
        ])
        return Response(self.get_serializer(test).data, status=201)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def answer(self, request, pk=None):
        test = self.get_object()
        if test.status != 'in_progress':
            return Response({'detail': 'This mock test is already finished.'}, status=400)

        if timezone.now() >= test.started_at + timedelta(minutes=test.duration_minutes):
            test.status = 'expired'
            test.completed_at = timezone.now()
            test.save(update_fields=['status', 'completed_at'])
            return Response({'detail': 'Mock test time has expired.'}, status=400)

        test_question = MockTestQuestion.objects.select_related('question').get(
            mock_test=test, question_id=request.data.get('question_id')
        )
        option = test_question.question.options.filter(id=request.data.get('option_id')).first()
        if option is None:
            return Response({'detail': 'Invalid option for this question.'}, status=400)

        test_question.selected_option = option
        test_question.is_correct = option.is_correct
        test_question.answered_at = timezone.now()
        test_question.save(update_fields=['selected_option', 'is_correct', 'answered_at'])

        test.attempted_questions = MockTestQuestion.objects.filter(mock_test=test, selected_option__isnull=False).count()
        test.correct_answers = MockTestQuestion.objects.filter(mock_test=test, is_correct=True).count()
        test.score = test.correct_answers
        test.save(update_fields=['attempted_questions', 'correct_answers', 'score'])
        return Response({'success': True, 'is_correct': test_question.is_correct})

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def submit(self, request, pk=None):
        test = self.get_object()
        if test.status != 'in_progress':
            return Response(self.get_serializer(test).data)

        now = timezone.now()
        expired = now >= test.started_at + timedelta(minutes=test.duration_minutes)
        test.attempted_questions = MockTestQuestion.objects.filter(mock_test=test, selected_option__isnull=False).count()
        test.correct_answers = MockTestQuestion.objects.filter(mock_test=test, is_correct=True).count()
        test.score = test.correct_answers
        test.status = 'expired' if expired else 'completed'
        test.completed_at = now
        test.save(update_fields=['attempted_questions', 'correct_answers', 'score', 'status', 'completed_at'])
        cache.delete('leaderboard:top5:v1')
        return Response(self.get_serializer(test).data)
