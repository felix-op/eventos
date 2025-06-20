from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .notification import Notification 

User = get_user_model() # Obtiene la instancia activa del modelo de usuario

# =======================
# Model: notification_user
# Description: Intermediate model for Many-to-Many relationship between User and Notification,
#              storing read status for each user.
# =======================
class Notification_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('notification', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.notification.title} ({'Leída' if self.is_read else 'No Leída'})"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
            return True
        return False

    def mark_as_unread(self):
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save()
            return True
        return False
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_read = False
            self.read_at = None
        
        super().save(*args, **kwargs)