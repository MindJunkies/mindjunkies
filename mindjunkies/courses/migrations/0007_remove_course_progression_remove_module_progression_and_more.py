# Generated by Django 5.1.7 on 2025-04-14 03:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0006_course_progression_module_progression"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="progression",
        ),
        migrations.RemoveField(
            model_name="module",
            name="progression",
        ),
        migrations.AddField(
            model_name="enrollment",
            name="progression",
            field=models.PositiveIntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
    ]
