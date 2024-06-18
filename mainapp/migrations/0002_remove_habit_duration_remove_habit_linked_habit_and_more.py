# Generated by Django 5.0.6 on 2024-06-15 05:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="habit",
            name="duration",
        ),
        migrations.RemoveField(
            model_name="habit",
            name="linked_habit",
        ),
        migrations.AddField(
            model_name="habit",
            name="related_habit",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"is_pleasant": True},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="related_to",
                to="mainapp.habit",
            ),
        ),
        migrations.AddField(
            model_name="habit",
            name="time_to_complete",
            field=models.PositiveIntegerField(default=120),
        ),
        migrations.AlterField(
            model_name="habit",
            name="periodicity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="habit",
            name="reward",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="habit",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
