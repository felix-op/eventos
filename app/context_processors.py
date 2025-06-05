from .models import Notification_user, PriorityLevel
from django.db.models import Case, When

def notificaciones_preview(request):
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
