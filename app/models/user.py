from django.contrib.auth.models import AbstractUser

# =======================
# Model: User
# =======================
class User(AbstractUser):

    def __str__(self):
        return self.username
    
    def update(self, username=None):
        if username:
            self.username = username
        self.save()
