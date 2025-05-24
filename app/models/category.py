from django.db import models

# =======================
# Model: Category
# Description: Event category used for classification.
# =======================
class Category(models.Model):
    name = models.CharField(max_length=20, blank = False)
    description = models.CharField(max_length=80, blank = False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name