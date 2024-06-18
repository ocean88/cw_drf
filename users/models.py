from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import Group, Permission


NULLABLE = {"blank": True, "null": True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    tg_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Телеграм ID",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
