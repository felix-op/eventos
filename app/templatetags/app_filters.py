from django import template
from ..models import Rating, Event, TicketState

register = template.Library()

@register.inclusion_tag('app/pages/rating_dashboard.html', takes_context=True)
def show_rating_dashboard(context):
    user = context['request'].user

    # Eventos para los que el usuario tiene tickets expirados.
    eligible_events = Event.objects.filter(
        event__user=user, 
        event__state=TicketState.EXPIRED
    ).distinct()

    # Obtenemos las calificaciones que el usuario ya ha hecho
    user_ratings_dict = {
        rating.event.id: rating 
        for rating in Rating.objects.filter(user=user)
    }

    events_to_rate = []
    completed_ratings = []

    for event in eligible_events:
        if event.id in user_ratings_dict:
            # Si el evento ya fue calificado, añade el objeto Rating a la lista de completados.
            completed_ratings.append(user_ratings_dict[event.id])
        else:
            # Si no, añade el objeto Event a la lista de pendientes.
            events_to_rate.append(event)
            
    return {
        'events_to_rate': events_to_rate,
        'completed_ratings': sorted(completed_ratings, key=lambda r: r.created_at, reverse=True)
    }