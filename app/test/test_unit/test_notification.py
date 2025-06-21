from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Notification, PriorityLevel, Notification_user

User = get_user_model()

class NotificationTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="usuarioPrueba1", password="Password1")

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
        self.assertIsNotNone(notification_prueba.created_at)
        self.assertIsNotNone(notification_prueba.priority, PriorityLevel.HIGH)

        # Probar que la cantidad de remitentes es igual a 1
        self.assertEqual(notification_prueba.recipients.count(), 1)

        # Probar que el remitente es el mismo
        primer_destinatario = notification_prueba.recipients.first()
        self.assertEqual(primer_destinatario, self.user1)

        self.assertEqual(self.user1.notifications_received.count(), 1)
        self.assertEqual(self.user1.notifications_received.first(), notification_prueba)

    def test_notification_validate_with_valid_data(self):
        priority = PriorityLevel.HIGH
        errors = Notification.validate("Titulo cargado prueba", "Mensaje cargado prueba", priority)
        self.assertEqual(errors, {})

    def test_notification_validate_with_empty_title(self):
        priority = PriorityLevel.HIGH
        errors = Notification.validate("", "Mensaje cargado prueba", priority)
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "Por favor ingrese un titulo")
    
    def test_notification_validate_with_none_message(self):
        priority = PriorityLevel.MEDIUM
        errors = Notification.validate("Titulo cargado prueba", None, priority)
        self.assertIn("message", errors)
        self.assertEqual(errors["message"], "Por favor ingrese un mensaje")

    def test_notification_validate_with_empty_priority(self):
        invalidate_priority = ""
        errors = Notification.validate("Titulo cargado prueba", "Mensaje cargado prueba", priority=invalidate_priority)
        self.assertIn("priority", errors)
        self.assertEqual(errors["priority"], "Nivel de prioridad no válido. Elija entre HIGH, MEDIUM o LOW.")

    def test_notification_new_with_valid_data(self):
        user2 = User.objects.create_user(username="usuarioPrueba2", password="Password2")
        user3 = User.objects.create_user(username="usuarioPrueba3", password="Password3")

        inicial_notification_count = Notification.objects.count()
        inicial_relation_count = Notification_user.objects.count()

        priority = PriorityLevel.LOW
        notification, errors = Notification.new(
            title="Titulo prueba nueva notification",
            message="Mensaje prueba nueva notification",
            priority=priority,
            recipient_users=[user2, user3]
        )

        # Sobre los valores
        self.assertTrue(notification)
        self.assertIsNone(errors, "No deberia haber errores")
        new_notification = Notification.objects.get(title="Titulo prueba nueva notification")
        self.assertEqual(new_notification.message, "Mensaje prueba nueva notification")
        self.assertIsInstance(notification, Notification, "El objeto devuelto debe ser una Notification")

        # Sobre la creación de objetos en DB
        self.assertEqual(Notification.objects.count(), inicial_notification_count + 1)
        self.assertEqual(Notification_user.objects.count(), inicial_relation_count + 2)

        # Sobre la relaciones creadas
        self.assertEqual(notification.recipients.count(), 2)

    def test_notification_not_new_with_invalid_data(self):
        inicial_notification_count = Notification.objects.count()
        priority = "INVALIDO"
        notification, errors = Notification.new(
            title="",
            message="Mensaje prueba nueva notification",
            priority=priority
        )

        self.assertIsNone(notification, "La notificación no debería haberse creado")
        self.assertIsNotNone(errors, "El diccionario de errores no debería ser None")
        self.assertIn("title", errors, "Debería haber un error en el campo 'title'")
        self.assertIn("priority", errors, "Debería haber un error en el campo 'priority'")

        final_notification_count = Notification.objects.count()
        self.assertEqual(final_notification_count, inicial_notification_count,
                        "La cantidad de notificaciones en la DB no debería haber cambiado")

    def test_notification_update_with_valid_data(self):
        notification = Notification.objects.create(
            title="Titulo original prueba notification",
            message="Mensaje original prueba notification",
            priority=PriorityLevel.MEDIUM
        )

        new_title="Titulo actualizado prueba notification"
        new_priority=PriorityLevel.HIGH

        update_notification, errors = notification.update(title=new_title, priority=new_priority)

        self.assertTrue(update_notification, "La actualización debería ser exitosa")
        self.assertIsNone(errors, "No debería haber errores")

        notification.refresh_from_db()
        self.assertEqual(notification.title, new_title)
        self.assertEqual(notification.priority, new_priority)
        self.assertEqual(notification.message, "Mensaje original prueba notification")

    def test_notification_not_update_with_invalid_data(self):
        original_title="Titulo original prueba notification"
        original_priority=PriorityLevel.MEDIUM
        notification = Notification.objects.create(
            title=original_title,
            message="Mensaje orignal prueba notification",
            priority=original_priority
        )

        update_notification, errors = notification.update(title="", priority="INVALIDO")

        self.assertFalse(update_notification, "La actualización debería haber fallado")
        self.assertIn("title", errors, "Debería haber un error en el campo 'title'")
        self.assertIn("priority", errors, "Debería haber un error en el campo 'priority'")

        notification.refresh_from_db()
        self.assertEqual(notification.title, original_title,
                        "No debería cambiar el titulo original en la DB")
        self.assertEqual(notification.priority, original_priority,
                        "No debería cambiar la prioridad original en la DB")
