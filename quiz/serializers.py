from rest_framework import serializers
from .models import (
    Category, SubCategory, PaperCategory, Question, Option, QuestionPaper,
    UserProgress, MockTest, MockTestQuestion,
)


class PaperCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperCategory
        fields = ['id', 'name', 'slug', 'description', 'image']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'description']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')
    sub_category_slug = serializers.ReadOnlyField(source='sub_category.slug')

    class Meta:
        model = Question
        fields = [
            'id', 'category', 'category_name', 'category_slug',
            'sub_category', 'sub_category_name', 'sub_category_slug',
            'text', 'explanation', 'options'
        ]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'subcategories']


class QuestionPaperSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = QuestionPaper
        fields = [
            'id', 'title', 'category', 'category_name', 'file',
            'image', 'description', 'uploaded_at'
        ]


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'question', 'is_correct', 'answered_at']
        read_only_fields = ['id', 'user', 'answered_at']


class MockTestQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    selected_option = OptionSerializer(read_only=True)

    class Meta:
        model = MockTestQuestion
        fields = [
            'id', 'question', 'question_order', 'selected_option',
            'is_correct', 'answered_at'
        ]


class MockTestSerializer(serializers.ModelSerializer):
    test_questions = MockTestQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = MockTest
        fields = [
            'id', 'title', 'duration_minutes', 'total_questions',
            'score', 'correct_answers', 'attempted_questions', 'status',
            'started_at', 'completed_at', 'test_questions'
        ]
        read_only_fields = fields
