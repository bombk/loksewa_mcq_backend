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

# Mock Test API
# GET    /api/quiz/mock-tests/
# POST   /api/quiz/mock-tests/
# GET    /api/quiz/mock-tests/<id>/
# POST   /api/quiz/mock-tests/<id>/answer/
# POST   /api/quiz/mock-tests/<id>/submit/
router.register(r'mock-tests', MockTestViewSet, basename='mocktest')

urlpatterns = [
    path('', include(router.urls)),
]
