from django.db import models

# =======================
# Model: Venue
# Description: Location where events are held, with capacity and contact info.
# =======================
class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=150)
    capacity = models.IntegerField()
    contact = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='static/media/venues', null=True, blank=True)


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