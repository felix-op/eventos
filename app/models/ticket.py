from django.db import models
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
    ticket_code = models.CharField(max_length=100)
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
    def validate(cls, quantity, ticket_code):
        errors = {}

        if quantity >= 30:
            errors["quantity"] = "No se pueden comprar mas de 30 entradas en un ticket"

        if len(ticket_code) >= 100:
            errors["ticket_code"] = "El codigo no puede ser mayor a 100 caracteres"


        return errors

    @property
    def has_refund(self):
        from . import RefundRequest
        return RefundRequest.objects.filter(ticket_code=self).exists()

    @classmethod
    def new(cls, buy_date,  ticket_code, quantity, type, state, user, event):
        errors = Ticket.validate(quantity,ticket_code)

        if len(errors.keys()) > 0:
            return False, errors

        cls.objects.create(
            buy_date,
            quantity = quantity,
            ticket_code = ticket_code,
            type = type,
            state = state,
            user = user,
            event = event
        )

        return True, None

    def update(self, quantity, type, state, user, event):
        self.quantity = quantity or self.quantity
        self.type = type or self.type
        self.state = state or self.state
        self.user = user or self.user
        self.event = event or self.event

        self.save()