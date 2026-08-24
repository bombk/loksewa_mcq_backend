from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Category, PaperCategory, Question, QuestionPaper, UserProgress
from .serializers import (
    CategorySerializer,
    PaperCategorySerializer,
    QuestionPaperSerializer,
    QuestionSerializer,
    UserProgressSerializer,
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
            if category.isdigit():
                queryset = queryset.filter(category_id=category)
            else:
                queryset = queryset.filter(category__slug=category)

        sub_category = self.request.query_params.get('sub_category')
        if sub_category:
            if sub_category.isdigit():
                queryset = queryset.filter(sub_category_id=sub_category)
            else:
                queryset = queryset.filter(sub_category__slug=sub_category)

        return queryset


class QuestionPaperViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionPaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = QuestionPaper.objects.filter(is_verified=True).select_related('category')
        category = self.request.query_params.get('category')
        if category:
            if category.isdigit():
                queryset = queryset.filter(category_id=category)
            else:
                queryset = queryset.filter(category__slug=category)
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
            total=Count('id'),
            correct=Count('id', filter=Q(is_correct=True)),
        )

        today = timezone.localdate()
        activity_log = []
        for offset in range(6, -1, -1):
            date = today - timedelta(days=offset)
            activity_log.append({
                'date': date.isoformat(),
                'count': progress.filter(answered_at__date=date).count(),
            })

        return Response({
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts,
            'category_stats': list(category_stats),
            'activity_log': activity_log,
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def leaderboard(self, request):
        from django.contrib.auth.models import User

        top_users = (
            User.objects.annotate(
                score=Count('progress', filter=Q(progress__is_correct=True))
            )
            .filter(score__gt=0)
            .order_by('-score', 'username')[:5]
        )

        return Response([
            {
                'username': user.username,
                'score': user.score,
                'profile_photo': (
                    request.build_absolute_uri(user.profile.profile_photo.url)
                    if hasattr(user, 'profile') and user.profile.profile_photo
                    else None
                ),
                'color_seed': len(user.username),
            }
            for user in top_users
        ])
