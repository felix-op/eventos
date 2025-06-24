from django.test import TestCase
from app.models import RefundRequest, Ticket, TicketState, TicketType, Event
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class RefundRequestTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="userPruebaR", password="Password123")
        self.event = Event.objects.create(
            title="Titulo prueba event",
            description="Description prueba event",
            date=timezone.now()
        )
        
        self.ticket = Ticket.objects.create(
            user=self.user,
            event=self.event,
            ticket_code = "EVT4-F119D7D2",
            type = TicketType.GENERAL,
            state = TicketState.VALID,
        )

    def test_refund_creation(self):
        initial_rating_count = RefundRequest.objects.count()

        refund_request = RefundRequest.objects.create(
            usuario=self.user,
            ticket_code=self.ticket,
            reason='event_cancelled'
        )

        self.assertEqual(RefundRequest.objects.count(), initial_rating_count + 1)

        self.assertEqual(refund_request.usuario, self.user)
        self.assertEqual(refund_request.ticket_code, self.ticket)
        self.assertEqual(refund_request.reason, 'event_cancelled')

        self.assertIsNone(refund_request.approved, "Al crearse, 'approved' debería ser None.")
        self.assertIsNone(refund_request.approval_date, "Al crearse, 'approval_date' debería ser None.")

        self.assertIsNotNone(refund_request.created_at)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.state, TicketState.VALID)

    def test_refund_approved_change_ticket_state_refunded(self):
        refund_request = RefundRequest.objects.create(
            usuario=self.user,
            ticket_code=self.ticket,
            reason='event_cancelled'
        )

        self.assertEqual(self.ticket.state, TicketState.VALID)

        refund_request.approved = True
        refund_request.save()

        self.assertTrue(refund_request.approved)
        self.assertIsNotNone(refund_request.approval_date)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.state, TicketState.REFUNDED)

    def test_refund_approved_change_ticket_state_expired(self):
        refund_request = RefundRequest.objects.create(
            usuario=self.user,
            ticket_code=self.ticket,
            reason='could_not_attend'
        )

        self.assertEqual(self.ticket.state, TicketState.VALID)

        refund_request.approved = False
        refund_request.save()

        self.assertFalse(refund_request.approved)
        self.assertIsNotNone(refund_request.approval_date)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.state, TicketState.EXPIRED)

    def test_refund_update_with_valid_data(self):
        refund_request = RefundRequest.objects.create(
            usuario=self.user,
            ticket_code=self.ticket,
            reason='other',
            reason_detail="Detalle original"
        )
        
        new_reason_detail = "Este es el nuevo detalle actualizado."
        refund_request.update(reason_detail=new_reason_detail)

        refund_request.refresh_from_db()
        self.assertEqual(refund_request.reason_detail, new_reason_detail)