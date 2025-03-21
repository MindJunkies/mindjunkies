# Generated by Django 5.1.7 on 2025-03-15 14:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forums", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="forumtopic",
            name="like_count",
        ),
        migrations.AddField(
            model_name="forumtopic",
            name="reaction",
            field=models.ManyToManyField(
                related_name="posts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
