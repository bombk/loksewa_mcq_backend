
import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User
from quiz.models import UserProgress, Question, Category

def seed_leaderboard():
    print("Seeding leaderboard data...")
    
    # ensure we have some questions
    if not Question.objects.exists():
        print("No questions found! Run seed_data.py first.")
        return

    questions = list(Question.objects.all())
    
    # Create or get dummy users
    dummy_users = [
        ('Aarav', 'aarav@example.com'),
        ('Binita', 'binita@example.com'),
        ('Chandra', 'chandra@example.com'),
        ('Deepa', 'deepa@example.com'),
        ('Eshan', 'eshan@example.com'),
        ('Gita', 'gita@example.com'),
    ]

    for username, email in dummy_users:
        user, created = User.objects.get_or_create(username=username, email=email)
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {username}")
        
        # Give them random progress
        # Clear existing
        UserProgress.objects.filter(user=user).delete()
        
        # Assign 5-20 random correct answers
        score_count = random.randint(5, 25)
        selected_qs = random.sample(questions, min(len(questions), score_count))
        
        for q in selected_qs:
            UserProgress.objects.create(
                user=user,
                question=q,
                is_correct=True
            )
    
    print("Leaderboard seeded successfully!")

if __name__ == "__main__":
    seed_leaderboard()
