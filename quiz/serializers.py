from rest_framework import serializers
from .models import Category, SubCategory, PaperCategory, Question, Option, QuestionPaper, UserProgress

class PaperCategorySerializer(serializers.ModelSerializer):
    paper_count = serializers.SerializerMethodField()

    class Meta:
        model = PaperCategory
        fields = ['id', 'name', 'description', 'image', 'paper_count']

    def get_paper_count(self, obj):
        return obj.papers.count()

class SubCategorySerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')
    
    class Meta:
        model = Question
        fields = ['id', 'category', 'category_name', 'sub_category', 'sub_category_name', 'text', 'explanation', 'options']

class CategorySerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'question_count', 'subcategories']

    def get_question_count(self, obj):
        return obj.questions.count()

class QuestionPaperSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = QuestionPaper
        fields = ['id', 'title', 'category', 'category_name', 'file', 'image', 'description', 'uploaded_at']

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'question', 'is_correct', 'answered_at']
        read_only_fields = ['id', 'user', 'answered_at']
