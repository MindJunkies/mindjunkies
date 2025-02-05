# Generated by Django 5.1.5 on 2025-02-04 20:42

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('short_introduction', models.CharField(max_length=500)),
                ('course_description', models.TextField()),
                ('course_image', models.ImageField(upload_to='course_images/')),
                ('preview_video_link', models.URLField(blank=True, null=True)),
                ('published', models.BooleanField(default=False)),
                ('upcoming', models.BooleanField(default=False)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('paid_course', models.BooleanField(default=False)),
                ('course_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('total_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('number_of_ratings', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClassroomTeacher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('teacher', 'Teacher'), ('assistant', 'Teaching Assistant')], default='teacher', max_length=10)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='classrooms.classroom')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='teaching_roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('classroom', 'teacher')},
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('pending', 'Pending'), ('withdrawn', 'Withdrawn')], default='pending', max_length=10)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='classrooms.classroom')),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, related_name='enrolled', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('classroom', 'student')},
            },
        ),
    ]
