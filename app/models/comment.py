from django.db import models

# =======================
# Model: Comment
# Description: User comment on an event, including a title and text.
# =======================
class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=750)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username} - {self.event.title}"
    
    @classmethod
    def validate(cls, title, text):
        errors = {}
        if not title:
            errors['title'] = 'El titulo no puede estar vacío'
        if not text:
            errors['text'] = 'El texto no puede estar vacio'
        return errors

    @classmethod
    def new(cls, user, event, title, text):
        errors = cls.validate(title, text)

        if errors:
            return False, errors
        
        comment_obj = cls.objects.create(
            user=user,
            event=event, 
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