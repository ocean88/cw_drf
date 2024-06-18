from unittest import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from mainapp.models import Habit
from users.models import User
from django.urls import reverse


class HabitViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user2@example.com")
        self.habit = Habit.objects.create(
            user=self.user, action="Test Habit", place="Test Place", time="12:00:00"
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrive(self):
        url = reverse("mainapp:habits-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Test Habit")

    def test_create_habit(self):
        url = reverse("mainapp:habits-list")
        data = {
            "user": self.user.pk,
            "action": "Test Habit",
            "place": "Test Place",
            "time": "12:00:00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_habit(self):
        url = reverse("mainapp:habits-detail", args=(self.habit.pk,))
        data = {
            "user": self.user.pk,
            "action": "Updated Test Habit",
            "place": "Updated Test Place",
            "time": "12:00:00",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Updated Test Habit")
        self.assertEqual(self.habit.place, "Updated Test Place")

    def test_delete_habit(self):
        url = reverse("mainapp:habits-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())

    def test_list_habit(self):
        url = reverse("mainapp:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
