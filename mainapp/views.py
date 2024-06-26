from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from mainapp.models import Habit
from mainapp.pagination import CustomPagination
from mainapp.serializer import HabitSerializer
from mainapp.permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema


class HabitViewSet(viewsets.ModelViewSet):
    """Контроллер для работы с привычками."""
    queryset = Habit.objects.all().order_by("id")
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["action", "place"]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(user=user)
        else:
            # Для анонимных пользователей показываем только публичные привычки или логику,
            # которая подходит для вашего приложения
            return Habit.objects.none() # Пример фильтрации по атрибуту public

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с публичными привычками.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["action", "place"]
    ordering_fields = ["id"]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Получение списка публичных привычек",
        responses={200: HabitSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получение публичной привычки",
        responses={200: HabitSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)

