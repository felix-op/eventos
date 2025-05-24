from django.db import models

# =======================
# Enum: UserType
# Description: Available user roles (admin, seller, client).
# =======================
class UserType(models.TextChoices):
    ADMINISTRADOR = 'admin', 'Administrador'
    VENDEDOR = 'vendedor', 'Vendedor'
    CLIENTE = 'cliente', 'Cliente'

# =======================
# Model: User
# Description: Custom user model with roles and notification settings.
# =======================
class User(models.Model):
    tipo = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.CLIENTE
    )
    username = models.CharField(max_length=100, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    notification = models.ManyToManyField('Notification', related_name='receptor')

    def __str__(self):
        return self.username

    def update(self, username=None):
        if username:
            self.username = username
        self.save()