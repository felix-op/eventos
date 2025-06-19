from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Event,Ticket,TicketState

class Command(BaseCommand):
    help = "Cambiar estado de tickets, si ya se realizo el evento"

    def handle(self, *args, **options):
        
        eventos_pasados = Event.objects.filter(
            date__lt = timezone.now(),
            _tickets_updated = False
        )
        
        if not eventos_pasados.exists():
            self.stdout.write(self.style.WARNING("No hay tickets para actualizar"))
            return

        for event in eventos_pasados:
            Ticket.objects.filter(
                event = event, 
                state = TicketState.VALID
            ).update(state = TicketState.EXPIRED)

            event._tickets_updated = True
            event.save()



        self.stdout.write(self.style.SUCCESS("Tickets actualizados"))