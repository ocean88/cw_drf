from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views
from mainapp.apps import MainappConfig
from mainapp.views import HabitViewSet, PublicHabitViewSet

app_name = MainappConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")
router.register(r"public-habits", PublicHabitViewSet, basename="public-habits")
urlpatterns = [] + router.urls
