from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BlogPost, Vacancy, VideoSource, HeroSlide, ContactMessage, ChatbotKnowledge, AnnouncementPopup, Book, BookCategory
from .serializers import (
    BlogPostSerializer, VacancySerializer, VideoSourceSerializer, 
    HeroSlideSerializer, ContactMessageSerializer, AnnouncementPopupSerializer, BookSerializer, BookCategorySerializer
)

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = None

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'company', 'description']

class VideoSourceViewSet(viewsets.ModelViewSet):
    queryset = VideoSource.objects.all()
    serializer_class = VideoSourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

class HeroSlideViewSet(viewsets.ModelViewSet):
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    http_method_names = ['post', 'get', 'delete'] # Limit to POST (frontend), GET/DELETE (admin via API if needed)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'description']

    def get_queryset(self):
        queryset = Book.objects.all().order_by('-created_at')
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class AnnouncementPopupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnnouncementPopup.objects.all()
    serializer_class = AnnouncementPopupSerializer

    def get_queryset(self):
        return AnnouncementPopup.objects.filter(is_active=True)

@api_view(['POST'])
def chatbot_response(request):
    user_message = request.data.get('message', '').lower()
    
    # Advanced Fuzzy Matching using FuzzyWuzzy
    from fuzzywuzzy import process, fuzz
    
    # Try to find a match in the knowledge base
    knowledge = ChatbotKnowledge.objects.all()
    if not knowledge.exists():
        return Response({'reply': "I'm still learning! Check back soon for more info."})

    # Prepare list of stored questions
    choices = {item.id: item.question.lower() for item in knowledge}
    
    # Find the best match
    # extractOne returns (match_string, score, key)
    match = process.extractOne(user_message, choices, scorer=fuzz.token_set_ratio)
    
    # Threshold for a "good" match: 60 is usually decent for token_set_ratio
    if match and match[1] >= 60:
        best_match = ChatbotKnowledge.objects.get(id=match[2])
        reply = best_match.answer
    elif 'quiz' in user_message or 'quizzes' in user_message:
        reply = "I can help with quizzes! Just ask about topics like 'Medical', 'Engineering', or 'Banking'."
    elif 'vacancy' in user_message or 'jobs' in user_message or 'job' in user_message:
        reply = "Looking for jobs? Ask me about 'Latest Vacancies' or 'Jobs'."
    else:
        # Fallback to general greeting if no high-confidence match
        reply = "I'm not exactly sure about that. Try searching for 'Free', 'Performance', or ask about 'Quizzes'."
        
    return Response({'reply': reply})
