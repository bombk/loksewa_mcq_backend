from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogPostViewSet, VacancyViewSet, VideoSourceViewSet, 
    HeroSlideViewSet, ContactMessageViewSet, chatbot_response,
    AnnouncementPopupViewSet, BookViewSet, BookCategoryViewSet
)

router = DefaultRouter()
router.register(r'blogs', BlogPostViewSet)
router.register(r'book-categories', BookCategoryViewSet)
router.register(r'vacancies', VacancyViewSet)
router.register(r'videos', VideoSourceViewSet)
router.register(r'hero-slides', HeroSlideViewSet)
router.register(r'contact-messages', ContactMessageViewSet, basename='contactmessage')
router.register(r'announcements', AnnouncementPopupViewSet, basename='announcement')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('chatbot/', chatbot_response),
]
