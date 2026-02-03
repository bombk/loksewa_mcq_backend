from rest_framework import serializers
from .models import BlogPost, Vacancy, VideoSource, HeroSlide, ContactMessage, AnnouncementPopup

class AnnouncementPopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementPopup
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'

class VideoSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSource
        fields = '__all__'

class HeroSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSlide
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
