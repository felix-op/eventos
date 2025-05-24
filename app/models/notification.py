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

        if title == "":
            errors["title"] = "Por favor ingrese un titulo"

        if message == "":
            errors["message"] = "Por favor ingrese un mensaje"

        if priority not in PriorityLevel.values:
            errors["priority"] = "Nivel de prioridad no válido. Elija entre HIGH, MEDIUM o LOW."
        return errors

    @classmethod
    def new(cls, title, message, priority, is_read=False):
        errors = Notification.validate(title, message, priority)

        if len(errors.keys()) > 0:
            return False, errors

        Notification.objects.create(
            title=title,
            message=message,
            priority=priority,
            is_read=is_read,
        )

        return True, None

    def update(self, title, message, priority, is_read):
        self.title = title or self.title
        self.message = message or self.message
        self.priority = priority or self.priority
        self.is_read = is_read or self.is_read

        self.save()