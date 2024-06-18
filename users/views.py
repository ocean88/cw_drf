from django.shortcuts import render
from users.models import User
from rest_framework.generics import CreateAPIView
from users.serializer import UserSerializer
from rest_framework.permissions import AllowAny


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


# Create your views here.
