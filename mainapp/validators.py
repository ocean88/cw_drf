from django.core.exceptions import ValidationError


def validate_no_simultaneous_reward_and_related_habit(habit):
    if habit.reward and habit.related_habit:
        raise ValidationError(
            "Нельзя одновременно указывать вознаграждение и связанную привычку."
        )


def validate_time_to_complete(habit):
    if habit.time_to_complete > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_related_habit(habit):
    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )


def validate_pleasant_habit(habit):
    if habit.is_pleasant:
        if habit.reward or habit.related_habit:
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


def validate_periodicity(habit):
    if habit.periodicity > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем раз в 7 дней.")
