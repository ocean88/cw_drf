from celery import shared_task
import requests
from datetime import datetime, timedelta
from django.conf import settings
from mainapp.models import Habit


def send_telegram_message(tg_chat_id, message):
    """Скелет для отправки сообщения в Telegram"""
    params = {
        "text": message,
        "chat_id": tg_chat_id,
    }
    response = requests.get(
        f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
        params=params,
    )
    if response.status_code == 200:
        return True
    else:
        return False


@shared_task
def check_habits_and_send_messages():
    """Периодическое напоминанение привычек"""
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    habits = Habit.objects.all()

    for habit in habits:
        habit_datetime = datetime.combine(current_date, habit.time)

        # Проверяем, если время привычки уже прошло и она не была отправлена сегодня
        if (
            habit_datetime <= current_datetime
            and not habit.is_sent
            and habit_datetime.date() == current_date
        ):
            message = f"Пропущенное напоминание: {habit.action} в {habit.place} в {habit.time}."
            if habit.reward:
                message += f" Награда: {habit.reward}."
            send_telegram_message(habit.user.tg_chat_id, message)
            habit.is_sent = True
            habit.save()
