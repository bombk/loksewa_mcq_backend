from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q
from .models import Category, Question, QuestionPaper, UserProgress
from .serializers import (
    CategorySerializer, QuestionSerializer, QuestionPaperSerializer, 
    UserProgressSerializer
)
from rest_framework import permissions

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class QuestionPaperViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionPaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        # Public users only see verified papers
        queryset = QuestionPaper.objects.filter(is_verified=True)
        
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset.order_by('-uploaded_at')

    def create(self, request, *args, **kwargs):
        # Allow anyone to upload, but it won't be verified by default
        return super().create(request, *args, **kwargs)

class UserProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProgressSerializer

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Update if exists, else create
        question = serializer.validated_data.get('question')
        is_correct = serializer.validated_data.get('is_correct')
        progress, created = UserProgress.objects.update_or_create(
            user=self.request.user,
            question=question,
            defaults={'is_correct': is_correct}
        )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = self.request.user
        progress = UserProgress.objects.filter(user=user)
        
        total_attempts = progress.count()
        correct_attempts = progress.filter(is_correct=True).count()
        
        # Category-wise breakdown
        category_stats = progress.values('question__category__name').annotate(
            total=Count('id'),
            correct=Count('id', filter=Q(is_correct=True))
        )
        
        # Last 7 days activity
        from django.utils import timezone
        import datetime
        last_7_days = []
        for i in range(7):
            date = timezone.now().date() - datetime.timedelta(days=i)
            count = progress.filter(answered_at__date=date).count()
            last_7_days.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        last_7_days.reverse()

        return Response({
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts,
            'category_stats': list(category_stats),
            'activity_log': last_7_days
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def leaderboard(self, request):
        from django.contrib.auth.models import User
        # Get top 5 users by correct answers
        top_users = User.objects.annotate(
            score=Count('progress', filter=Q(progress__is_correct=True))
        ).filter(score__gt=0).order_by('-score')[:5]

        data = []
        for user in top_users:
            profile_photo = None
            if hasattr(user, 'profile') and user.profile.profile_photo:
                profile_photo = request.build_absolute_uri(user.profile.profile_photo.url)
            
            data.append({
                'username': user.username,
                'score': user.score,
                'profile_photo': profile_photo,
                'color_seed': len(user.username) 
            })
        
        return Response(data)
