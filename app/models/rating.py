from django.db import models

# =======================
# Model: Rating
# Description: User-generated rating for an event (1 to 5 scale).
# =======================
class Rating(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
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