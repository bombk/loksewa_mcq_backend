from rest_framework import serializers
from .models import BlogPost, Vacancy, VideoSource, HeroSlide, ContactMessage, AnnouncementPopup, Book, BookCategory

class BookCategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = BookCategory
        fields = ['id', 'name', 'description', 'image', 'book_count']

    def get_book_count(self, obj):
        return obj.books.count()

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'category_name', 'cover_image', 'pdf_file', 'description', 'created_at']

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
