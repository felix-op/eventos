from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Notification, Notification_user
from django.utils import timezone

User = get_user_model()

class NotificationUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="usuarioPrueba7", password="Password7")
        self.notification = Notification.objects.create(title="Titulo notification prueba")

    def test_create_default_not_read(self):
        relation = Notification_user.objects.create(
            user=self.user,
            notification=self.notification
        )

        self.assertFalse(relation.is_read)
        self.assertIsNone(relation.read_at)
    
    def test_mark_as_read_valid(self):
        relation = Notification_user.objects.create(
            user=self.user,
            notification=self.notification
        )

        self.assertFalse(relation.is_read)

        result = relation.mark_as_read()

        self.assertTrue(result)

        self.assertTrue(relation.is_read)
        self.assertIsNotNone(relation.read_at)

    def test_mark_as_unread_valid(self):
        relation = Notification_user.objects.create(
            user=self.user,
            notification=self.notification
        )

        self.assertFalse(relation.is_read)

        result = relation.mark_as_unread()

        self.assertFalse(result)

        relation.refresh_from_db()
        self.assertFalse(relation.is_read)
        self.assertIsNone(relation.read_at)
