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
    
    @classmethod
    def validate(cls, name, description):
        errors = {}

        if not name or name.strip() == "":
            errors["name"] = "El nombre no puede estar vacío"

        if not description or description.strip() == "":
            errors["description"] = "La descripción no puede estar vacía"

        return errors

    @classmethod
    def new(cls, name, description, is_active=False):
        errors = cls.validate(name, description)
        if errors:
            return False, errors

        category = cls.objects.create(name=name, description=description, is_active=is_active)
        return True, category

    def update(self, name=None, description=None, is_active=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if is_active is not None:
            self.is_active = is_active
        self.save()