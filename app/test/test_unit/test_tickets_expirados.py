from django.test import TestCase
from django.utils import timezone
from django.core.management import call_command
from datetime import timedelta
from app.models import Event, User, Ticket, TicketState, TicketType

class ExpireTicketsTest(TestCase):
    def setUp(self):

        self.user = User.objects.create(username="testUser", password="Password123")

        self.evento_pasado = Event.objects.create(
            title = "evento pasado",
            description = "evento pasado",
            date = timezone.now() - timedelta(days=1)
        )
        
        Ticket.objects.create(
            ticket_code = "pasado1",
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.evento_pasado
        )

        Ticket.objects.create(
            ticket_code = "pasado2",
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.evento_pasado
        )

        self.evento_futuro = Event.objects.create(
            title = "evento futuro",
            description = "evento duturo",
            date = timezone.now() + timedelta(days=1)
        )

        Ticket.objects.create(
            ticket_code = "futuro1",
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.evento_futuro
        )

    def test_command(self):

        call_command('tickets_expirados')

        self.evento_pasado.refresh_from_db() # si no lo pongo, no detecta el cambio de _tickets_update a TRUE

        self.assertEqual(
            Ticket.objects.filter(event=self.evento_pasado, state=TicketState.EXPIRED).count(),
            2
        )

        # verificar si _tickets_updated es true
        
        self.assertTrue(self.evento_pasado._tickets_updated)

        # verificar si el evento futuro sigue igual
        self.assertEqual(
            Ticket.objects.filter(event= self.evento_futuro, state=TicketState.VALID).count(),
            1
        )
