import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from content.models import ChatbotKnowledge

def seed_chatbot():
    qa_pairs = [
        {"question": "How to take a quiz?", "answer": "To take a quiz, simply go to the 'Quiz' page, select a category like 'Administration' or 'Engineering', and click on any sub-category to start practicing!"},
        {"question": "How can I see my performance?", "answer": "You can see your performance charts by clicking on your profile icon in the navbar. It shows your overall accuracy and category-wise mastery."},
        {"question": "Can I upload my own papers?", "answer": "Yes! Go to the 'All Questions' tab and use the upload form to share your PDF or Photo question papers with the community."},
        {"question": "How many categories are there?", "answer": "We have several professional categories including Administration, Engineering, Medical, Banking, and Teaching, with thousands of MCQs."},
        {"question": "Is the platform free?", "answer": "Yes, our MCQ platform is completely free to use for all students and career seekers!"},
    ]

    for pair in qa_pairs:
        ChatbotKnowledge.objects.update_or_create(
            question=pair["question"],
            defaults={"answer": pair["answer"]}
        )
    print("Chatbot knowledge base seeded successfully!")

if __name__ == "__main__":
    seed_chatbot()
