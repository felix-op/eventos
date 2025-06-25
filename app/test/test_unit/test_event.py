from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Event, Category, Venue
from django.utils import timezone

User = get_user_model()

"""
def test_event_validate_with_valid_data(self):
    # Test que verifica la validación de eventos con datos válidos
    date = timezone.now() + datetime.timedelta(days=1)
    errors = Event.validate("Título válido", "Descripción válida", date)
    self.assertEqual(errors, {})

def test_event_validate_with_empty_title(self):
    # Test que verifica la validación de eventos con título vacío
    date = timezone.now() + datetime.timedelta(days=1)
    errors = Event.validate("", "Descripción válida", date)
    self.assertIn("title", errors)
    self.assertEqual(errors["title"], "Por favor ingrese un titulo")

def test_event_validate_with_empty_description(self):
    # Test que verifica la validación de eventos con descripción vacía
    date = timezone.now() + datetime.timedelta(days=1)
    errors = Event.validate("Título válido", "", date)
    self.assertIn("description", errors)
    self.assertEqual(errors["description"], "Por favor ingrese una descripcion")
"""

class TestEventValidation(TestCase):
    def test_validate_all_fields_empty(self):
        pass
    def test_validate_title_only(self):
        pass
    def test_validate_description_only(self):
        pass
    def test_validate_valid_data(self):
        pass

"""
def test_event_new_with_valid_data(self):
    # Test que verifica la creación de eventos con datos válidos
    date = timezone.now() + datetime.timedelta(days=2)
    success, errors = Event.new(
        title="Nuevo evento",
        description="Descripción del nuevo evento",
        date=date,
    )
    self.assertTrue(success)
    self.assertIsNone(errors)
    new_event = Event.objects.get(title="Nuevo evento")
    self.assertEqual(new_event.description, "Descripción del nuevo evento")

def test_event_new_with_invalid_data(self):
    # Test que verifica que no se crean eventos con datos inválidos
    date = timezone.now() + datetime.timedelta(days=2)
    initial_count = Event.objects.count()
    success, errors = Event.new(
        title="",
        description="Descripción del evento",
        date=date,
    )
    self.assertFalse(success)
    self.assertIn("title", errors)
    self.assertEqual(Event.objects.count(), initial_count)
"""


class TestEventCreation(TestCase):
    def test_new_with_invalide_data(self):
        pass
    def test_new_with_valid_data(self):
        pass

"""
def test_event_update(self):
    # Test que verifica la actualización de eventos
    new_title = "Título actualizado"
    new_description = "Descripción actualizada"
    new_date = timezone.now() + datetime.timedelta(days=3)
    event = Event.objects.create(
        title="Evento de prueba",
        description="Descripción del evento de prueba",
        date=timezone.now() + datetime.timedelta(days=1),
    )
    event.update(
        title=new_title,
        description=new_description,
        date=new_date,
    )
    updated_event = Event.objects.get(pk=event.pk)
    self.assertEqual(updated_event.title, new_title)
    self.assertEqual(updated_event.description, new_description)
    self.assertEqual(updated_event.date.time(), new_date.time())

def test_event_update_partial(self):
    # Test que verifica la actualización parcial de eventos
    event = Event.objects.create(
        title="Evento de prueba",
        description="Descripción del evento de prueba",
        date=timezone.now() + datetime.timedelta(days=1),
    )
    original_title = event.title
    original_date = event.date
    new_description = "Solo la descripción ha cambiado"
    event.update(
        title=None,
        description=new_description,
        date=None,
    )
    updated_event = Event.objects.get(pk=event.pk)
    self.assertEqual(updated_event.title, original_title)
    self.assertEqual(updated_event.description, new_description)
    self.assertEqual(updated_event.date, original_date)
"""


class TestEventUpdate(TestCase):
    def test_update_all_fields(self):
        pass
    def test_update_partial_fields(self):
        pass

class TestEventAverageRating(TestCase):
    def test_average_rating_with_no_ratings(self):
        pass
    def test_average_rating_with_multiple_rating(self):
        pass

class TestEventStr(TestCase):
    def test_str_returns_title(self):
        pass

class TestEventRelationships(TestCase):
    def test_event_can_have_categories(self):
        pass
    def test_event_can_have_venue(self):
        pass
    def test_event_image_optional(self):
        pass