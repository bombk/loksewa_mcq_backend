import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from quiz.models import Category, SubCategory, PaperCategory

def generate_unique_slug(model, name):
    base_slug = slugify(name) or "slug"
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

for category in Category.objects.filter(slug__isnull=True) | Category.objects.filter(slug=""):
    category.slug = generate_unique_slug(Category, category.name)
    category.save(update_fields=['slug'])

for sub_category in SubCategory.objects.filter(slug__isnull=True) | SubCategory.objects.filter(slug=""):
    sub_category.slug = generate_unique_slug(SubCategory, sub_category.name)
    sub_category.save(update_fields=['slug'])

for paper_category in PaperCategory.objects.filter(slug__isnull=True) | PaperCategory.objects.filter(slug=""):
    paper_category.slug = generate_unique_slug(PaperCategory, paper_category.name)
    paper_category.save(update_fields=['slug'])

print("Slugs backfilled successfully.")
