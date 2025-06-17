from django import template
from ..models import Rating, Event, TicketState

register = template.Library()

@register.inclusion_tag('app/pages/rating_dashboard.html', takes_context=True)
def show_rating_dashboard(context):
    user = context['request'].user

    # 1. Obtenemos los eventos para los que el usuario tiene tickets expirados.
    #    Esta es nuestra lista de "eventos elegibles".
    eligible_events = Event.objects.filter(
        event__user=user, 
        event__state=TicketState.EXPIRED
    ).distinct()

    # 2. Obtenemos las calificaciones que el usuario ya ha hecho en un diccionario.
    #    La clave será el ID del evento, para una búsqueda rápida.
    user_ratings_dict = {
        rating.event.id: rating 
        for rating in Rating.objects.filter(user=user)
    }

    # 3. Creamos nuestras dos listas: una para pendientes y otra para completados.
    events_to_rate = []
    completed_ratings = []

    for event in eligible_events:
        if event.id in user_ratings_dict:
            # Si el evento ya fue calificado, añadimos el objeto Rating a la lista de completados.
            completed_ratings.append(user_ratings_dict[event.id])
        else:
            # Si no, añadimos el objeto Event a la lista de pendientes.
            events_to_rate.append(event)
            
    # 4. Devolvemos AMBAS listas al contexto de la plantilla.
    return {
        'events_to_rate': events_to_rate,
        'completed_ratings': sorted(completed_ratings, key=lambda r: r.created_at, reverse=True)
    }