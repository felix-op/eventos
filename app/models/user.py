from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# =======================
# Enum: UserType
# Description: Available user roles (admin, seller, client).
# =======================

#class UserType(models.TextChoices):
# ADMINISTRADOR = 'admin', 'Administrador'
#  VENDEDOR = 'vendedor', 'Vendedor'
#   CLIENTE = 'cliente', 'Cliente'
#
# =======================
# Custom UserManager
# =======================

# =======================
# Model: User
# =======================
class User(AbstractUser):
   # objects = UserManager()  # <- Usamos el UserManager personalizado

    def __str__(self):
        return self.username
    
    def update(self, username=None):
        if username:
            self.username = username
        self.save()
