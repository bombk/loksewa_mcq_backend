
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from content.models import AnnouncementPopup

def seed_announcement():
    # Deactivate existing
    AnnouncementPopup.objects.all().update(is_active=False)

    # Create new active one
    AnnouncementPopup.objects.create(
        title="🎉 Big Update: New Quizzes!",
        content="We've just added 50+ new questions to the Engineering section. Check them out and boost your skills today!",
        is_active=True,
        is_public=True
    )
    print("Seeded active announcement.")

if __name__ == "__main__":
    seed_announcement()
