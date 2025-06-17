from django.db import models
from django.db.models import Avg

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