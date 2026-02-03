from django.contrib import admin
from .models import Category, Question, Option, QuestionPaper

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_verified', 'uploaded_at')
    list_filter = ('is_verified', 'category')
    search_fields = ('title', 'description')
    actions = ['verify_papers']
    fields = ('title', 'category', 'file', 'image', 'description', 'is_verified')

    def verify_papers(self, request, queryset):
        queryset.update(is_verified=True)
    verify_papers.short_description = "Verify selected question papers"

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category')
    list_filter = ('category',)
    search_fields = ('text', 'explanation')
    inlines = [OptionInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__category')
    search_fields = ('text',)
