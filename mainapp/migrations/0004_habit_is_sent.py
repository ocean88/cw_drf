# Generated by Django 5.0.6 on 2024-06-16 08:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0003_alter_habit_related_habit"),
    ]

    operations = [
        migrations.AddField(
            model_name="habit",
            name="is_sent",
            field=models.BooleanField(default=False),
        ),
    ]
