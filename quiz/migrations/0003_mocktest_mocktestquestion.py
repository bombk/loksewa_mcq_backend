from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0002_papercategory_questionpaper_subcategory_userprogress_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Mock Test', max_length=255)),
                ('duration_minutes', models.PositiveIntegerField(default=60)),
                ('total_questions', models.PositiveIntegerField(default=100)),
                ('score', models.PositiveIntegerField(default=0)),
                ('correct_answers', models.PositiveIntegerField(default=0)),
                ('attempted_questions', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('expired', 'Expired')], default='in_progress', max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mock_tests', to='auth.user')),
            ],
            options={
                'indexes': [
                    models.Index(fields=['user', '-started_at'], name='quiz_mocktes_user_id_5e1c3e_idx'),
                    models.Index(fields=['user', 'status'], name='quiz_mocktes_user_id_8a5c0d_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='MockTestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField(default=False)),
                ('answered_at', models.DateTimeField(blank=True, null=True)),
                ('question_order', models.PositiveIntegerField()),
                ('mock_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_questions', to='quiz.mocktest')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mock_test_questions', to='quiz.question')),
                ('selected_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mock_test_answers', to='quiz.option')),
            ],
            options={
                'indexes': [
                    models.Index(fields=['mock_test', 'question_order'], name='quiz_mocktes_mock_t_7d1e1b_idx'),
                    models.Index(fields=['mock_test', 'is_correct'], name='quiz_mocktes_mock_t_9a8b72_idx'),
                ],
                'constraints': [
                    models.UniqueConstraint(fields=('mock_test', 'question'), name='unique_mock_test_question'),
                    models.UniqueConstraint(fields=('mock_test', 'question_order'), name='unique_mock_test_question_order'),
                ],
            },
        ),
    ]
