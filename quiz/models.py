from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=['category', 'slug'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category.name} - {self.name}'


class Question(models.Model):
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, related_name='questions', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    explanation = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'id']),
            models.Index(fields=['sub_category', 'id']),
        ]

    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['question'])]

    def __str__(self):
        return self.text


class PaperCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='paper_category_images/', blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class QuestionPaper(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(PaperCategory, on_delete=models.CASCADE, related_name='papers')
    file = models.FileField(upload_to='question_papers/')
    image = models.ImageField(upload_to='question_papers/images/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['is_verified', '-uploaded_at'])]

    def __str__(self):
        return self.title


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_user_question_progress')
        ]
        indexes = [
            models.Index(fields=['user', 'answered_at']),
            models.Index(fields=['user', 'is_correct']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:20]} - {'Correct' if self.is_correct else 'Incorrect'}"
