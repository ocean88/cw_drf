from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_no_simultaneous_reward_and_related_habit,
    validate_time_to_complete,
    validate_related_habit,
    validate_pleasant_habit,
    validate_periodicity,
)


class HabitSerializer(serializers.ModelSerializer):
    """Настройки валидаторов для модели Habit"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"
        extra_kwargs = {
            "user": {"write_only": True},  # чтобы поле user не было видимым в запросах
            "related_habit": {"allow_null": True},
        }

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            validated_data["user"] = self.context["request"].user
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Пользователь не авторизован")

    def update(self, instance, validated_data):
        if self.context["request"].user.is_authenticated:
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("Пользователь не авторизован")

    def validate(self, data):
        # Получаем экземпляр Habit из входных данных
        habit_instance = Habit(**data)

        # Вызываем ваши валидаторы, передавая экземпляр Habit
        validate_no_simultaneous_reward_and_related_habit(habit_instance)
        validate_time_to_complete(habit_instance)
        validate_related_habit(habit_instance)
        validate_pleasant_habit(habit_instance)
        validate_periodicity(habit_instance)

        return data
