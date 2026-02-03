from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogPostViewSet, VacancyViewSet, VideoSourceViewSet, 
    HeroSlideViewSet, ContactMessageViewSet, chatbot_response,
    AnnouncementPopupViewSet
)

router = DefaultRouter()
router.register(r'blogs', BlogPostViewSet)
router.register(r'vacancies', VacancyViewSet)
router.register(r'videos', VideoSourceViewSet)
router.register(r'hero-slides', HeroSlideViewSet)
router.register(r'contact-messages', ContactMessageViewSet, basename='contactmessage')
router.register(r'announcements', AnnouncementPopupViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
    path('chatbot/', chatbot_response),
]
