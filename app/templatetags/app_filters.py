from django import template
from ..models import Ticket, Rating, Event, TicketState

register = template.Library()

@register.inclusion_tag('app/pages/rating_dashboard.html', takes_context=True)
def show_rating_dashboard(context):
    user = context['request'].user
    # Primera consulta: obtener los ticket de los eventos que compro y expiraron
    expired_ticket_event_pks = Ticket.objects.filter(
        user=user,
        state=TicketState.EXPIRED
    ).values_list('event__pk', flat=True) # flat es para obtener tuplas en vez de instancias
    
    user_rated_event_pks = Rating.objects.filter(
        user=user
    ).values_list('event__pk', flat=True)

    events_to_rate = Event.objects.filter(
        pk__in=expired_ticket_event_pks
    ).exclude(
        pk__in=user_rated_event_pks
    ).distinct().order_by('-date')
    
    return {
        'events_to_rate':events_to_rate
    }