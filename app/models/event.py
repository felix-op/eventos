from django.db import models
from django.db.models import Avg, Sum
from django.utils import timezone

# =======================
# Model: Event
# Description: Represents an event with a title, description, and scheduled date.
# =======================
class Event(models.Model):
    categories = models.ManyToManyField("Category", related_name="events", blank=True)
    venue = models.ForeignKey("Venue", on_delete=models.PROTECT, null=True)
    imagen = models.ImageField(upload_to='events/', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _tickets_updated = models.BooleanField(default=False) # _ hace que sea privado

    def __str__(self):
        return self.title

    @classmethod
    def validate(cls, title, description, date):
        errors = {}

        if title == "":
            errors["title"] = "Por favor ingrese un titulo coherente"

        if description == "":
            errors["description"] = "Por favor ingrese una descripcion útil"

        if not date:
            errors["date"] = "Por favor ingrese una fecha con sentido"
        elif date < timezone.now():
            errors["date"] = "La fecha no puede estar en el pasado >:|"

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

    @property
    def average_rating(self):
        return self.rating_set.aggregate(avg=Avg('rating'))['avg'] or 0