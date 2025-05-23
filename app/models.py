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
<<<<<<< HEAD

        
=======
# ===========   User      =================
class User(models.Model):
    ADMINISTRADOR = 'admin'
    VENDEDOR = 'vendedor'
    CLIENTE = 'cliente'

    TIPOS_USUARIO = [
        (ADMINISTRADOR, 'Administrador'),
        (VENDEDOR, 'Vendedor'),
        (CLIENTE, 'Cliente'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPOS_USUARIO, default=CLIENTE)
    username = models.CharField(max_length=100, blank=False, unique=True)
    email = models.EmailField(blank=False,unique=True)
    notification = models.ManyToManyField('Notification', related_name='receptor')

    def __str__(self):
        return self.username

    def update(self, username=None):
        if username:
            self.username = username
        self.save() 
>>>>>>> 6f8e9a0c0ee5a69b87ca6aeab18efef9d99e4cf6
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
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.rating}/5"

    @classmethod
    def validate(cls, title, text, rating):
        errors = {}

        if not title:
            errors["title"] = "El título no puede estar vacío"

        if not text:
            errors["text"] = "El texto no puede estar vacío"

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            errors["rating"] = "La calificación debe estar entre 1 y 5"

        return errors

    @classmethod
    def new(cls, user, event, title, text, rating):
        errors = cls.validate(title, text, rating)

        if errors:
            return False, errors

        rating_obj = cls.objects.create(
            user=user,
            event=event,
            title=title,
            text=text,
            rating=rating
        )

        return True, rating_obj

    def update(self, title=None, text=None, rating=None):
        if title is not None:
            self.title = title
        if text is not None:
            self.text = text
        if rating is not None and (1 <= rating <= 5):
            self.rating = rating

        self.save()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=750)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @classmethod
    def validate(cls, title, text):
        errors = {}
        if not title:
            errors['title'] = 'El titulo no puede estar vacío'
        if not text:
            errors['text'] = 'El texto no puede estar vacio'
        return errors

    @classmethod
    def new(cls, user, title, text):
        errors = cls.validate(title, text)

        if errors:
            return False, errors
        
        comment_obj = cls.objects.create(
            user=user,
            title=title,
            text=text
        )

        return True, comment_obj

    def update(self, title=None, text=None):
        if title is not None:
            self.title = title
        if text is not None:
            self.text = text
        self.save()
<<<<<<< HEAD

## Modelo NOTIFICATION = NOTIFICACION

class Priority_level(models.TextChoices):
    HIGH = 'HIGH', 'High'
    MEDIUM = 'MEDIUM', 'Medium'
    LOW = 'LOW', 'Low'

class Notification(models.Model):
    title = models.CharField(max_length=150)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add = True)
    priority = models.CharField(max_length=6, 
        choices=Priority_level.choices, default = Priority_level.LOW)
    is_read = models.BooleanField(default = False)
    
    def __str__(self):
        return self.title
    
    @classmethod
    def validate(cls, title, message, priority):
        errors = {}

        if title == "":
            errors["title"] = "Por favor ingrese un titulo"

        if message == "":
            errors["message"] = "Por favor ingrese un mensaje"

        if priority not in Priority_level.values:
            errors["priority"] = "Nivel de prioridad no válido. Elija entre HIGH, MEDIUM o LOW."
        return errors

    @classmethod
    def new(cls, title, message, priority, is_read=False):
        errors = Notification.validate(title, message, priority)

        if len(errors.keys()) > 0:
            return False, errors

        Notification.objects.create(
            title=title,
            message=message,
            priority=priority,
            is_read=is_read,
        )

        return True, None

    def update(self, title, message, priority, is_read):
        self.title = title or self.title
        self.message = message or self.message
        self.priority = priority or self.priority
        self.is_read = is_read or self.is_read

        self.save()

## Modelo VENUE = LUGAR DE ENCUENTRO
class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=150)
    capacity = models.IntegerField()
    contact = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

    @classmethod
    def validate(cls, name, address, city, capacity, contact):
        errors = {}

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if address == "":
            errors["address"] = "Por favor ingrese una dirección"
            
        if city == "":
            errors["city"] = "Por favor ingrese una ciudad"

        if capacity == None or capacity == 0:
            errors["capacity"] = "Por favor ingrese una capacidad (núm. +)"
        
        if contact == "":
            errors["contact"] = "Por favor ingrese un contacto"
        
        return errors

    @classmethod
    def new(cls, name, address, city, capacity, contact):
        errors = Venue.validate(name, address, city, capacity, contact)

        if len(errors.keys()) > 0:
            return False, errors

        Venue.objects.create(
            name=name,
            address=address,
            city=city,
            capacity=capacity,
            contact=contact,
        )

        return True, None

    def update(self, name, address, city, capacity, contact):
        self.name = name or self.name
        self.address = address or self.address
        self.city = city or self.city
        self.capacity = capacity or self.capacity
        self.contact =contact or self.contact

        self.save()

=======
# ===========   RefundRequest      =================
class RefundRequest(models.Model):
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    ticket_code = models.CharField(max_length=100, blank=False)
    reason = models.CharField(max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_code

    def update(self, approved=None, reason=None, approval_date=None):
        if approved is not None:
            self.approved = approved
        if reason is not None:
            self.reason = reason
        if approval_date is not None:
            self.approval_date = approval_date
        self.save()
>>>>>>> 6f8e9a0c0ee5a69b87ca6aeab18efef9d99e4cf6
