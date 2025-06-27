from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Event, Category, Venue, Rating
from django.utils import timezone
import datetime

User = get_user_model()

class TestEventValidation(TestCase):
    def test_validate_all_fields_empty(self):
        date = timezone.now() + datetime.timedelta(days=1)
        errors = Event.validate("", "", date)
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "Por favor ingrese un titulo coherente")
        self.assertIn("description", errors)
        self.assertEqual(errors["description"], "Por favor ingrese una descripcion útil")

    def test_validate_title_only(self):
        date = timezone.now() + datetime.timedelta(days=1)
        errors = Event.validate("Título pasable", "", date)
        self.assertIn("description", errors)
        self.assertEqual(errors["description"], "Por favor ingrese una descripcion útil")
        self.assertNotIn("title", errors)

    def test_validate_description_only(self):
        date = timezone.now() + datetime.timedelta(days=1)
        errors = Event.validate("", "Descripción increible", date)
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "Por favor ingrese un titulo coherente")
        self.assertNotIn("description", errors)

    def test_validate_valid_data(self):
        date = timezone.now() + datetime.timedelta(days=1)
        errors = Event.validate("Título único", "Descripción epica", date)
        self.assertEqual(errors, {})

    def test_validate_with_past_date(self):
        date = timezone.now() - datetime.timedelta(days=1)
        errors = Event.validate("Título", "Descripción", date)
        self.assertIn("date", errors)
        self.assertEqual(errors["date"], "La fecha no puede estar en el pasado >:|")

    def test_validate_with_missing_date(self):
        errors = Event.validate("Título", "Descripción", None)
        self.assertIn("date", errors)
        self.assertEqual(errors["date"], "Por favor ingrese una fecha con sentido")


class TestEventCreation(TestCase):
    def test_new_with_invalid_data(self):
        date = timezone.now() + datetime.timedelta(days=2)
        initial_count = Event.objects.count()
        success, errors = Event.new(
            title="",
            description="Descripción basura",
            date=date,
        )
        self.assertFalse(success)
        self.assertIn("title", errors)
        self.assertEqual(Event.objects.count(), initial_count)

    def test_new_with_valid_data(self):
        date = timezone.now() + datetime.timedelta(days=2)
        success, errors = Event.new(
            title="Evento inentendible",
            description="Descripción incomprensible",
            date=date,
        )
        self.assertTrue(success)
        self.assertIsNone(errors)
        new_event = Event.objects.get(title="Evento inentendible")
        self.assertEqual(new_event.description, "Descripción incomprensible")


class TestEventUpdate(TestCase):
    def test_update_all_fields(self):
        new_title = "Título espectacular"
        new_description = "Descripción espectacular"
        new_date = timezone.now() + datetime.timedelta(days=3)

        event = Event.objects.create(
            title="Titulo común",
            description="Descripción común",
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

    def test_update_partial_fields(self):
        event = Event.objects.create(
            title="Que importa",
            description="Nadie lo lee",
            date=timezone.now() + datetime.timedelta(days=1)
        )

        original_title = event.title
        original_date = event.date
        new_description = "Nadie lo usa"
    
        event.update(
            title=None,
            description=new_description,
            date=None,
        )

        updated_event = Event.objects.get(pk=event.pk)
        self.assertEqual(updated_event.title, original_title)
        self.assertEqual(updated_event.description, new_description)
        self.assertEqual(updated_event.date, original_date)


class TestEventAverageRating(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')

    def test_average_rating_with_no_ratings(self):
        event = Event.objects.create(
            title="Evento sin ratings",
            description="Un evento sin calificaciones",
            date=timezone.now() + datetime.timedelta(days=1)
        )
        self.assertEqual(event.average_rating, 0)

    def test_average_rating_with_multiple_rating(self):
        event = Event.objects.create(
            title="Evento con ratings",
            description="Un evento calificado",
            date=timezone.now() + datetime.timedelta(days=1)
        )

        Rating.objects.create(event=event, user=self.user, rating=4, title="Buena", text="Muy buen evento")
        Rating.objects.create(event=event, user=self.user, rating=5, title="Excelente", text="Me encantó")
        Rating.objects.create(event=event, user=self.user, rating=3, title="Regular", text="Podría mejorar")

        expected_avg = (4 + 5 + 3) / 3
        self.assertAlmostEqual(event.average_rating, expected_avg)

class TestEventStr(TestCase):
    def test_str_returns_title(self):
        event = Event.objects.create(
            title="Título visible",
            description="No importa para este test",
            date=timezone.now() + datetime.timedelta(days=1)
        )
        self.assertEqual(str(event), "Título visible")

class TestEventRelationships(TestCase):
    def test_event_can_have_categories(self):
        event = Event.objects.create(
            title="Evento con categoría",
            description="Prueba de categoría",
            date=timezone.now() + datetime.timedelta(days=1)
        )
        cat1 = Category.objects.create(name="Música", description="Conciertos")
        cat2 = Category.objects.create(name="Arte", description="Galerías")

        event.categories.add(cat1, cat2)
        self.assertEqual(event.categories.count(), 2)
        self.assertIn(cat1, event.categories.all())
        self.assertIn(cat2, event.categories.all())
    
    def test_event_can_have_venue(self):
        venue = Venue.objects.create(
            name="Universidad Nacional Tierra del Fuego",
            address="Hipólito Yrigoyen 879",
            city="Ushuaia",
            capacity=500,
            contact="contacto@teatrocolon.ar"
        )

        event = Event.objects.create(
            title="Concierto",
            description="Música clásica",
            date=timezone.now() + datetime.timedelta(days=1),
            venue=venue
        )

        self.assertEqual(event.venue.name, "Universidad Nacional Tierra del Fuego")


    def test_event_image_optional(self):
        event = Event.objects.create(
            title="Evento sin imagen",
            description="Este evento no tiene imagen",
            date=timezone.now() + datetime.timedelta(days=1)
        )
        self.assertIsNone(event.imagen.name)