from .models import Notification_user
# Contexto Global para mantener el contador de notificaciones sin leer
# Esto evita tener que colocar en cada vista un
# context['notifications'] = Notification_user.objects.unread_for_user(request.user).count

def unread_notifications(request):
    if request.user.is_authenticated:
        unread_count = Notification_user.objects.unread_for_user(request.user).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count}