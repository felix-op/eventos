# users/signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(m2m_changed, sender=User.groups.through)
def update_is_staff(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Si se pone al usuario como admin se la permiso de staff y superuser
        if instance.groups.filter(name='admin').exists():
            instance.is_staff = True
            instance.is_superuser = True
        # Si se pone al usuario como seller se la permiso de staff
        elif instance.groups.filter(name='seller').exists():
            instance.is_staff = True
            instance.is_superuser = False
        # Si no es ni admin ni seller pierde sus permisos
        else:
            instance.is_staff = False
            instance.is_superuser = False
        
        instance.save()
