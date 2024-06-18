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
        """
        Получение списка привычек для аутентифицированных пользователей.
        """
        if self.request.user.is_authenticated:
            return Habit.objects.filter(user=self.request.user)
        else:
            return Habit.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Создание привычки",
        request_body=HabitSerializer,
        responses={201: HabitSerializer()},
    )
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise ValidationError("У вас нет прав.")
        serializer.save()

    @swagger_auto_schema(
        operation_description="Удаление привычки",
        responses={204: "No Content"},
    )
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise ValidationError("У вас нет прав.")
        instance.delete()


class PublicHabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с публичными привычками.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["action", "place"]
    ordering_fields = ["id"]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Получение списка публичных привычек",
        responses={200: HabitSerializer(many=True)},
    )
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if Habit.objects.filter(is_public=True).exists():
                return Habit.objects.filter(is_public=True)
            else:
                return Habit.objects.filter(user=user)
        else:
            return Habit.objects.none()

    @swagger_auto_schema(
        operation_description="Получение списка публичных привычек или привычек пользователя",
        responses={200: HabitSerializer(many=True)},
    )
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]

    @swagger_auto_schema(
        operation_description="Создание публичной привычки",
        request_body=HabitSerializer,
        responses={201: HabitSerializer()},
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
