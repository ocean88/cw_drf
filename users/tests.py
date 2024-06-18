from django.test import TestCase

from users.models import User


# Create your tests here.
class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123',
            'tg_chat_id': '123456789'
        }

    def test_create_user(self):
        user = User.objects.create(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.tg_chat_id, self.user_data['tg_chat_id'])
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)