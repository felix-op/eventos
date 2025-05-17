from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def validate(cls, title, description, date):
        errors = {}

        if title == "":
            errors["title"] = "Por favor ingrese un titulo"

        if description == "":
            errors["description"] = "Por favor ingrese una descripcion"

        return errors

    @classmethod
    def new(cls, title, description, date):
        errors = Event.validate(title, description, date)

        if len(errors.keys()) > 0:
            return False, errors

        Event.objects.create(
            title=title,
            description=description,
            date=date,
        )

        return True, None

    def update(self, title, description, date):
        self.title = title or self.title
        self.description = description or self.description
        self.date = date or self.date

        self.save()
        
# ===========   TICKET      =================

class Ticket_type(models.IntegerChoices):
    GENERAL = 1, 'General'
    VIP = 2, 'Vip'

class Ticket_state(models.IntegerChoices):
    VALID = 1, 'Valid'
    EXPIRED = 2, 'Expired'
    REFUNDED = 3, 'Refunded'

class Ticket(models.Model):
    buy_date = models.DateTimeField(auto_now_add=True)
    ticket_code = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    type = models.IntegerField(
        choices = Ticket_type.choices,
        null = False,
        blank = False
    )
    state = models.IntegerField(
        choices = Ticket_state.choices,
        null = False, 
        blank = False
    )
    #   RELACIONES
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank = False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event', blank = False)

    def __str__(self):
        return self.ticket_code
    
    @classmethod
    def validate(cls, quantity, ticket_code):
        errors = {}

        if quantity >= 30:
            errors["quantity"] = "No se pueden comprar mas de 30 entradas en un ticket"

        if ticket_code >= 100:
            errors["ticket_code"] = "El codigo no puede ser mayor a 100 caracteres"


        return errors

    @classmethod
    def new(cls, buy_date,  ticket_code, quantity, type, state, user, event):
        errors = Ticket.validate(quantity,ticket_code)

        if len(errors.keys()) > 0:
            return False, errors

        Event.objects.create(
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

# ===========   CATEGORY      =================
class Category(models.Model):
    name = models.CharField(max_length=20, blank = False)
    description = models.CharField(max_length=80, blank = False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name