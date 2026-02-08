from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, PaperCategoryViewSet, QuestionViewSet, 
    QuestionPaperViewSet, UserProgressViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'paper-categories', PaperCategoryViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'papers', QuestionPaperViewSet, basename='questionpaper')
router.register(r'progress', UserProgressViewSet, basename='userprogress')

urlpatterns = [
    path('', include(router.urls)),
]
