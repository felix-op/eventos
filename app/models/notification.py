from django.db import models
from django.contrib.auth import get_user_model # Importa la forma correcta de obtener el User model
from django.core.exceptions import ValidationError

User = get_user_model() # Obtiene la instancia activa del modelo de usuario

# =======================
# Enum: PriorityLevel
# Description: Priority levels for notifications (High, Medium, Low).
# =======================
class PriorityLevel(models.TextChoices):
    HIGH = 'HIGH', 'High'
    MEDIUM = 'MEDIUM', 'Medium'
    LOW = 'LOW', 'Low'

# =======================
# Model: Notification
# Description: System notification for users, includes priority and read state.
# =======================
class Notification(models.Model):
    title = models.CharField(max_length=150)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add = True)
    priority = models.CharField(max_length=6, 
        choices=PriorityLevel.choices, default = PriorityLevel.LOW)
    recipients = models.ManyToManyField(
        User,
        through='app.Notification_user', # Especifica el modelo intermedio
        related_name='notifications_received',
        blank=True
    )
    
    def __str__(self):
        return self.title

    def clean(self):
        errors = {}
        if not self.title:
            errors["title"] = ValidationError("Por favor ingrese un titulo", code='required')

        if not self.message: 
            errors["message"] = ValidationError("Por favor ingrese un mensaje", code='required')

        if self.priority not in PriorityLevel.values:
            errors["priority"] = ValidationError("Nivel de prioridad no válido. Elija entre HIGH, MEDIUM o LOW.", code='required')
        
        if errors:
            raise ValidationError(errors)
        
    @classmethod
    def validate(cls, title, message, priority):
        errors = {}

        if not title:
            errors["title"] = "Por favor ingrese un titulo"

        if not message: 
            errors["message"] = "Por favor ingrese un mensaje"

        if priority not in PriorityLevel.values:
            errors["priority"] = "Nivel de prioridad no válido. Elija entre HIGH, MEDIUM o LOW."
        return errors

    @classmethod
    def new(cls, title, message, priority, recipient_users=[]):

        errors = Notification.validate(title, message, priority)

        if errors:
            return None, errors

        notification = cls.objects.create(
            title=title,
            message=message,
            priority=priority,
        )

        from app.models.notification_user import Notification_user
        
        for user in recipient_users:
            Notification_user.objects.create(
                user=user,
                notification=notification,
                is_read=False # Por defecto, no leída
            )

        return notification, None # Devuelve el objeto creado

    def update(self, title=None, message=None, priority=None):
        updated_fields = {}
        if title is not None:
            updated_fields['title'] = title
        if message is not None:
            updated_fields['message'] = message
        if priority is not None:
            updated_fields['priority'] = priority

        temp_title = updated_fields.get('title', self.title)
        temp_message = updated_fields.get('message', self.message)
        temp_priority = updated_fields.get('priority', self.priority)

        errors = self.validate(temp_title, temp_message, temp_priority)

        if errors:
            return False, errors 

        for field, value in updated_fields.items():
            setattr(self, field, value)

        self.save()
        return True, None