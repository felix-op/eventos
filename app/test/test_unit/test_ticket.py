import datetime

from django.test import TestCase
from django.utils import timezone

from app.models import Ticket, TicketState, TicketType, User, Event


class TicketModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testUser", password="Password123")
        self.event = Event.objects.create(title="Evento x", description="descripcion", date=timezone.now())

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            ticket_code = "EVT4-F119D7D2",
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )
        self.assertEqual(ticket.ticket_code, "EVT4-F119D7D2")
        self.assertEqual(ticket.type, TicketType.GENERAL)
        self.assertEqual(ticket.state, TicketState.VALID)
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.event, self.event)
        self.assertEqual(ticket.quantity, 1)
        self.assertIsNotNone(ticket.buy_date)
        self.assertEqual(ticket.quantity, 1)

    def test_ticket_update(self):

        ticket = Ticket.objects.create(
            ticket_code = "EVT4-F119D7D2",
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )

        auxUser = User.objects.create(username="aux us", password="Password123")
        auxEvent = Event.objects.create(title="Evento y", description="descripcion", date=timezone.now())


        ticket.update(
            quantity = 20,
            type = TicketType.VIP,
            state = TicketState.REFUNDED,
            user = auxUser,
            event = auxEvent
        )

        self.assertEqual(ticket.quantity, 20)
        self.assertEqual(ticket.type, TicketType.VIP)
        self.assertEqual(ticket.state, TicketState.REFUNDED)
        self.assertEqual(ticket.user, auxUser)
        self.assertEqual(ticket.event, auxEvent)

    def test_ticket_update_parcial(self):

        ticket = Ticket.objects.create(
            ticket_code = "EVT4-F119D7D2",
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )

        ticket.update(
            quantity = 20,
            state = TicketState.REFUNDED,
        )

        self.assertEqual(ticket.quantity, 20)
        self.assertEqual(ticket.type, TicketType.GENERAL)
        self.assertEqual(ticket.state, TicketState.REFUNDED)
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.event, self.event)

    def test_invalid_quantity_max(self):
        success, errors = Ticket.new(
            ticket_code = "EVT4-F119D7D2",
            quantity = 31,
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )

        self.assertFalse(success)
        self.assertIn("quantity", errors)
        self.assertIn(errors["quantity"], "no se pueden comprar mas de 30 tickets")

    def test_invalid_quantity_min(self):
        success, errors = Ticket.new(
            ticket_code = "EVT4-F119D7D2",
            quantity = 0,
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )

        self.assertFalse(success)
        self.assertIn("quantity", errors)
        self.assertEqual(errors["quantity"], "Debe comprar al menos un ticket")
 
    def test_duplicate_code(self):
        
        Ticket.objects.create(
            ticket_code = "codigo1",
            quantity = 1,
            type = TicketType.GENERAL,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )

        success, errors = Ticket.new(
            ticket_code = "codigo1",
            quantity = 3,
            type = TicketType.VIP,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )

        self.assertFalse(success)
        self.assertIn("ticket_code", errors)

    def test_invalid_state(self):
        
        success, errors = Ticket.new(
            ticket_code = "EVT4-F119D7D2",
            quantity = 1,
            type = TicketType.GENERAL,
            state = 111,
            user = self.user,
            event = self.event
        )
        
        self.assertFalse(success)
        self.assertIn("state",errors)
    
    def test_invalid_type(self):
        
        success, errors = Ticket.new(
            ticket_code = "EVT4-F119D7D2",
            quantity = 1,
            type = 111,
            state = TicketState.VALID,
            user = self.user,
            event = self.event
        )
        
        self.assertFalse(success)
        self.assertIn("type",errors)