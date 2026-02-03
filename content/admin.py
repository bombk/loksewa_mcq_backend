from django.contrib import admin
from .models import BlogPost, Vacancy, VideoSource, HeroSlide, ContactMessage, ChatbotKnowledge, AnnouncementPopup

@admin.register(AnnouncementPopup)
class AnnouncementPopupAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title', 'content')

@admin.register(ChatbotKnowledge)
class ChatbotKnowledgeAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'deadline', 'created_at')
    search_fields = ('title', 'company', 'description')
    list_filter = ('deadline', 'company')

@admin.register(VideoSource)
class VideoSourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url', 'created_at')
    search_fields = ('title', 'description')

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'quote')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
