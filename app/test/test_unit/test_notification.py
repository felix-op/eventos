from django.test import TestCase
from django.contrib.auth import get_user_model

from eventos import app
from .models import Notification, PriorityLevel

User = get_user_model()

class NotificationTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="usuarioPrueba1", password="Password123")

        self.notification = Notification.objects.create(
            title = "Este es un titulo de prueba",
            message = "Este es un mensaje de prueba",
            priority = PriorityLevel.HIGH
        )

        self.notification.recipients.add(self.user1)
    
    def test_notification_creation(self):
        notification_prueba = Notification.objects.get(id=self.notification.id)

        self.assertEqual(notification_prueba.title,"Este es un titulo de prueba")
        self.assertEqual(notification_prueba.message, "Este es un mensaje de prueba")
        self.assertIsNone(notification_prueba.created_at)
        self.assertIsNotNone(notification_prueba.priority, PriorityLevel.HIGH)

        self.assertEqual(notification_prueba.recipients.count(), 1)

        primer_destinatario = notification_prueba.recipients.first()
        self.assertEqual(primer_destinatario, self.user1)

        self.assertEqual(self.user1.notifications_received.count(), 1)
        self.assertEqual(self.user1.notifications_received.first(), notification_prueba)
