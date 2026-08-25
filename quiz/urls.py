from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    MockTestViewSet,
    PaperCategoryViewSet,
    QuestionPaperViewSet,
    QuestionViewSet,
    UserProgressViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'paper-categories', PaperCategoryViewSet)
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'papers', QuestionPaperViewSet, basename='questionpaper')
router.register(r'progress', UserProgressViewSet, basename='userprogress')
router.register(r'mock-tests', MockTestViewSet, basename='mocktest')

urlpatterns = [
    path('', include(router.urls)),
]
