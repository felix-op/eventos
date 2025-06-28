from django.db import models, IntegrityError
from . import Event
from django.utils import timezone


# =======================
# Enum: TicketType
# Description: Enum for ticket categories (General, VIP).
# =======================
class TicketType(models.IntegerChoices):
    GENERAL = 1, 'General'
    VIP = 2, 'Vip'

# =======================
# Enum: TicketState
# Description: Enum for ticket status (Valid, Expired, Refunded).
# =======================
class TicketState(models.IntegerChoices):
    VALID = 1, 'Valid'
    EXPIRED = 2, 'Expired'
    REFUNDED = 3, 'Refunded'

# =======================
# Model: Ticket
# Description: Represents a ticket purchase linked to an event and a user.
# =======================
class Ticket(models.Model):
    buy_date = models.DateTimeField(auto_now_add=True)
    ticket_code = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField(default=1)
    type = models.IntegerField(
        choices = TicketType.choices,
        null = False,
        blank = False
    )
    state = models.IntegerField(
        choices = TicketState.choices,
        null = False, 
        blank = False
    )
    #   RELACIONES
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='user', blank = False)
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='event', blank = False)

    def __str__(self):
        return f"{self.ticket_code} - {self.user.username} - {self.event.title}"

    @classmethod
    def validate(cls, quantity=None, user=None, event=None, state=None, type=None):
        errors = {}

        if quantity is not None:
            if quantity > 30:
                errors["quantity"] = "no se pueden comprar mas de 30 tickets"
            elif quantity <= 0:
                errors["quantity"] = "Debe comprar al menos un ticket"

        if user is not None and not user: #verifica falsy
            errors["user"] = "Debe estar asociado a un usuario"

        if event is not None and not event: #verifica falsy
            errors["event"] = "Debe estar asociado a un evento"

        if state is not None and state not in [choice.value for choice in TicketState]:
            errors["state"] = "Estado de ticket invalido"

        if type is not None and type not in [choice.value for choice in TicketType]:
            errors["type"] = "Tipo de ticket invalido"

        return errors


    @property
    def has_refund(self):
        from . import RefundRequest
        return RefundRequest.objects.filter(ticket_code=self).exists()

    @property
    def solicitudRechazada(self):
        from . import RefundRequest
        return RefundRequest.objects.get(ticket_code=self).approved is False

    @classmethod
    def new(cls, ticket_code, quantity, type, state, user, event):
        errors = Ticket.validate(quantity,user,event,state,type)

        if len(errors.keys()) > 0:
            return False, errors

        try:
            cls.objects.create(
                quantity = quantity,
                ticket_code = ticket_code,
                type = type,
                state = state,
                user = user,
                event = event
            )

            return True, None
        except IntegrityError:
            return False, {"ticket_code": "Ya existe un ticket con ese codigo."}

    def update(self, quantity=None, type=None, state=None, user=None, event=None):
        if quantity is not None:
            self.quantity = quantity
        if type is not None:
            self.type = type
        if state is not None:
            self.state = state
        if user is not None:
            self.user = user
        if event is not None:
            self.event = event

        self.save()
