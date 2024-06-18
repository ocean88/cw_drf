# Generated by Django 5.0.6 on 2024-06-15 18:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_options_remove_user_username_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tg_chat_id",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Телеграм ID"
            ),
        ),
    ]