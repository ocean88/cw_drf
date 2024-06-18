from django.db import models
from config import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="related_to",
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=255, null=True, blank=True)
    time_to_complete = models.PositiveIntegerField(default=120)
    is_public = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    last_sent_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - я буду {self.action} в {self.time} в {self.place}"
