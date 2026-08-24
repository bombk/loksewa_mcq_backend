from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0011_category_slug_papercategory_slug_subcategory_slug'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='subcategory',
            index=models.Index(fields=['category', 'slug'], name='quiz_subcat_cat_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['category', 'id'], name='quiz_question_cat_id_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['sub_category', 'id'], name='quiz_question_subcat_id_idx'),
        ),
        migrations.AddIndex(
            model_name='option',
            index=models.Index(fields=['question'], name='quiz_option_question_idx'),
        ),
        migrations.AddIndex(
            model_name='questionpaper',
            index=models.Index(fields=['is_verified', '-uploaded_at'], name='quiz_paper_verified_date_idx'),
        ),
        migrations.AddIndex(
            model_name='userprogress',
            index=models.Index(fields=['user', 'answered_at'], name='quiz_progress_user_date_idx'),
        ),
        migrations.AddIndex(
            model_name='userprogress',
            index=models.Index(fields=['user', 'is_correct'], name='quiz_progress_user_correct_idx'),
        ),
    ]
