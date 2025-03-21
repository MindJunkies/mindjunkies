# Generated by Django 5.1.7 on 2025-03-08 09:14

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_remove_course_learning_objectives_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="course_image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="course_images/"
            ),
        ),
    ]
