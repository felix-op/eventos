from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Event, Category, Venue
from django.utils import timezone

User = get_user_model()

class EventModelTest(TestCase):
    def setUp(self):
        self.categories = Category.objects.create(
            name="Categ. Prueba",
            descripcion="Descripcion categoria prueba",
        )
        self.venue = Venue.objects.create(
            name="Nombre lugar prueba",
            address="Direccion prueba lugar",
            city="Ciudad prueba lugar",
            capacity=100,
            contact="Contacto prueba lugar"
        )

    def test_event_creation(self):
        event = Event.objects.create(
            categories=self.categories,
            venue=self.venue,
            title="Evento de prueba",
            description="Descripción del evento de prueba",
            date=timezone.now(),
        )
    # De aca para atras en teoria podria servirte, lo demas para abajo tenes que hacerlo vos, felix xd
    
        """Test que verifica la creación correcta de eventos"""
        self.assertEqual(event.title, "Evento de prueba")
        self.assertEqual(event.description, "Descripción del evento de prueba")
        self.assertIsNotNone(event.created_at)
        self.assertIsNotNone(event.updated_at)
        self.assertIsNotNone(event._tickets_updated)

    def test_event_validate_with_valid_data(self):
        """Test que verifica la validación de eventos con datos válidos"""
        date = timezone.now() + datetime.timedelta(days=1)
        errors = Event.validate("Título válido", "Descripción válida", date)
        self.assertEqual(errors, {})

    def test_event_validate_with_empty_title(self):
        """Test que verifica la validación de eventos con título vacío"""
        date = timezone.now() + datetime.timedelta(days=1)
        errors = Event.validate("", "Descripción válida", date)
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "Por favor ingrese un titulo")

    def test_event_validate_with_empty_description(self):
        """Test que verifica la validación de eventos con descripción vacía"""
        date = timezone.now() + datetime.timedelta(days=1)
        errors = Event.validate("Título válido", "", date)
        self.assertIn("description", errors)
        self.assertEqual(errors["description"], "Por favor ingrese una descripcion")

    def test_event_new_with_valid_data(self):
        """Test que verifica la creación de eventos con datos válidos"""
        date = timezone.now() + datetime.timedelta(days=2)
        success, errors = Event.new(
            title="Nuevo evento",
            description="Descripción del nuevo evento",
            date=date,
        )

        self.assertTrue(success)
        self.assertIsNone(errors)

        # Verificar que el evento fue creado en la base de datos
        new_event = Event.objects.get(title="Nuevo evento")
        self.assertEqual(new_event.description, "Descripción del nuevo evento")

    def test_event_new_with_invalid_data(self):
        """Test que verifica que no se crean eventos con datos inválidos"""
        date = timezone.now() + datetime.timedelta(days=2)
        initial_count = Event.objects.count()

        # Intentar crear evento con título vacío
        success, errors = Event.new(
            title="",
            description="Descripción del evento",
            date=date,
        )

        self.assertFalse(success)
        self.assertIn("title", errors)

        # Verificar que no se creó ningún evento nuevo
        self.assertEqual(Event.objects.count(), initial_count)

    def test_event_update(self):
        """Test que verifica la actualización de eventos"""
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

        # Recargar el evento desde la base de datos
        updated_event = Event.objects.get(pk=event.pk)

        self.assertEqual(updated_event.title, new_title)
        self.assertEqual(updated_event.description, new_description)
        self.assertEqual(updated_event.date.time(), new_date.time())

    def test_event_update_partial(self):
        """Test que verifica la actualización parcial de eventos"""
        event = Event.objects.create(
            title="Evento de prueba",
            description="Descripción del evento de prueba",
            date=timezone.now() + datetime.timedelta(days=1),
        )

        original_title = event.title
        original_date = event.date
        new_description = "Solo la descripción ha cambiado"

        event.update(
            title=None,  # No cambiar
            description=new_description,
            date=None,  # No cambiar
        )

        # Recargar el evento desde la base de datos
        updated_event = Event.objects.get(pk=event.pk)

        # Verificar que solo cambió la descripción
        self.assertEqual(updated_event.title, original_title)
        self.assertEqual(updated_event.description, new_description)
        self.assertEqual(updated_event.date, original_date)
