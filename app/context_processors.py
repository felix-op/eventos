from .models import Notification_user, PriorityLevel
from django.db.models import Case, When
# Contexto Global para mantener el contador de notificaciones sin leer
# Esto evita tener que colocar en cada vista un
# context['notifications'] = Notification_user.objects.unread_for_user(request.user).count

def unread_notifications(request):
    if request.user.is_authenticated:
        unread_count = Notification_user.objects.unread_for_user(request.user).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count}

def preview_notifications(request):
    notis_preview = []
    if request.user.is_authenticated:
        notis_preview = Notification_user.objects.filter(
            user=request.user
        ).select_related('notification').annotate(
            priority_orden=Case(
                When(notification__priority=PriorityLevel.HIGH, then=1),
                When(notification__priority=PriorityLevel.MEDIUM, then=2),
                When(notification__priority=PriorityLevel.LOW, then=3),
            )
        ).order_by('priority_orden', '-notification__created_at')[:5]
    
    return {'notis_preview': notis_preview}