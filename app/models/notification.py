from django.db import models

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
    is_read = models.BooleanField(default = False)
    
    def __str__(self):
        return self.title
    
    @classmethod
    def validate(cls, title, message, priority):
        errors = {}

        if not title: # Verifica si la cadena está vacía o es None
            errors["title"] = "Por favor ingrese un titulo"

        if not message: # Verifica si la cadena está vacía o es None
            errors["message"] = "Por favor ingrese un mensaje"

        if priority not in PriorityLevel.values:
            errors["priority"] = "Nivel de prioridad no válido. Elija entre HIGH, MEDIUM o LOW."
        return errors

    @classmethod
    def new(cls, title, message, priority, is_read=False):
        errors = Notification.validate(title, message, priority)

        if errors: # Verifica si el diccionario de errores no está vacío
            return False, errors

        notification = cls.objects.create( # Usa cls para consistencia
            title=title,
            message=message,
            priority=priority,
            is_read=is_read,
        )

        return True, notification # Devuelve el objeto creado

    def update(self, title=None, message=None, priority=None, is_read=None):
        # Crea un diccionario de campos a actualizar, excluyendo valores None
        updated_fields = {}
        if title is not None:
            updated_fields['title'] = title
        if message is not None:
            updated_fields['message'] = message
        if priority is not None:
            updated_fields['priority'] = priority
        if is_read is not None:
            updated_fields['is_read'] = is_read

        # Valida los cambios potenciales
        # Combina los valores actuales con las actualizaciones propuestas para la validación
        temp_title = updated_fields.get('title', self.title)
        temp_message = updated_fields.get('message', self.message)
        temp_priority = updated_fields.get('priority', self.priority)

        errors = self.validate(temp_title, temp_message, temp_priority)

        if errors:
            return False, errors # Devuelve False y errores si la validación falla

        for field, value in updated_fields.items():
            setattr(self, field, value)

        self.save()
        return True, None # Devuelve True en caso de éxito