from django.test import TestCase
from app.models import Venue

class VenueModelTest(TestCase):

    def test_venue_creation(self):

        # Crear un Venue válido
        venue = Venue.objects.create(
            name="Estadio Central",
            address="Av. Principal 123",
            city="Buenos Aires",
            capacity=5000,
            contact="contacto@estadio.com"
        )

        # Verificar que los campos se guardaron correctamente
        self.assertEqual(venue.name, "Estadio Central")
        self.assertEqual(venue.address, "Av. Principal 123")
        self.assertEqual(venue.city, "Buenos Aires")
        self.assertEqual(venue.capacity, 5000)
        self.assertEqual(venue.contact, "contacto@estadio.com")
        
        # Verificar que se haya guardado en la base de datos
        self.assertIsNotNone(venue.id)  # El ID debería existir después de la creación

    def test_venue_creation_invalid(self):
    # Contamos cuántos objetos `Venue` hay antes de intentar crear uno
        initial_count = Venue.objects.count()
    # Intentar crear un Venue con datos inválidos 
        success, errors = Venue.new(
        name="",  # Nombre vacío
        address="Av. Principal 123",
        city="Buenos Aires",
        capacity=0,  # Capacidad inválida
        contact="contacto@estadio.com"
    )

    # Verificar que la creación falla
        self.assertFalse(success)
        self.assertIn("name", errors)
        self.assertIn("capacity", errors)
        self.assertEqual(errors["name"], "Por favor ingrese un nombre")
        self.assertEqual(errors["capacity"], "Por favor ingrese una capacidad (núm. +)")

        # Asegurarse de que no se guardó en la base de datos
        self.assertEqual(Venue.objects.count(), initial_count)

    def test_venue_update(self):
        """Test que verifica la actualización completa de un Venue"""

        # Crear un Venue inicial
        venue = Venue.objects.create(
            name="Estadio Viejo",
            address="Calle 123",
            city="Rosario",
            capacity=3000,
            contact="contacto@viejo.com"
        )

        # Nuevos valores para actualizar
        new_name = "Estadio Nuevo"
        new_address = "Avenida Siempre Viva 742"
        new_city = "Córdoba"
        new_capacity = 10000
        new_contact = "nuevo@estadio.com"

        # Llamar al método update() del modelo
        venue.update(
            name=new_name,
            address=new_address,
            city=new_city,
            capacity=new_capacity,
            contact=new_contact
        )

        # Refrescar desde la base de datos
        updated_venue = Venue.objects.get(pk=venue.pk)

        # Verificar los cambios
        self.assertEqual(updated_venue.name, new_name)
        self.assertEqual(updated_venue.address, new_address)
        self.assertEqual(updated_venue.city, new_city)
        self.assertEqual(updated_venue.capacity, new_capacity)
        self.assertEqual(updated_venue.contact, new_contact)

    def test_venue_update_partial(self):

        venue = Venue.objects.create(
            name="Microestadio",
            address="Calle 456",
            city="La Plata",
            capacity=2000,
            contact="info@micro.com"
        )

        new_contact = "nuevo_contacto@micro.com"

        venue.update(
            name=None,
            address=None,
            city=None,
            capacity=None,
            contact=new_contact
        )

        updated_venue = Venue.objects.get(pk=venue.pk)

        # Solo debe haber cambiado el contacto
        self.assertEqual(updated_venue.name, "Microestadio")
        self.assertEqual(updated_venue.address, "Calle 456")
        self.assertEqual(updated_venue.city, "La Plata")
        self.assertEqual(updated_venue.capacity, 2000)
        self.assertEqual(updated_venue.contact, new_contact)

    def test_venue_validate_with_valid_data(self):
        """Test que verifica que la validación acepta datos válidos"""
        errors = Venue.validate("Luna Park", "Bouchard 465", "Buenos Aires", 5000, "info@lunapark.com")
        self.assertEqual(errors, {})

    def test_venue_validate_empty_name(self):
        """Test que verifica que el nombre vacío da error"""
        errors = Venue.validate("", "Dirección", "Ciudad", 1000, "contacto@test.com")
        self.assertIn("name", errors)
        self.assertEqual(errors["name"], "Por favor ingrese un nombre")

    def test_venue_validate_empty_address(self):
        """Test que verifica que la dirección vacía da error"""
        errors = Venue.validate("Nombre", "", "Ciudad", 1000, "contacto@test.com")
        self.assertIn("address", errors)
        self.assertEqual(errors["address"], "Por favor ingrese una dirección")

    def test_venue_validate_empty_city(self):
        """Test que verifica que la ciudad vacía da error"""
        errors = Venue.validate("Nombre", "Dirección", "", 1000, "contacto@test.com")
        self.assertIn("city", errors)
        self.assertEqual(errors["city"], "Por favor ingrese una ciudad")

    def test_venue_validate_invalid_capacity(self):
        """Test que verifica que la capacidad 0 da error"""
        errors = Venue.validate("Nombre", "Dirección", "Ciudad", 0, "contacto@test.com")
        self.assertIn("capacity", errors)
        self.assertEqual(errors["capacity"], "Por favor ingrese una capacidad (núm. +)")

    def test_venue_validate_empty_contact(self):
        """Test que verifica que el contacto vacío da error"""
        errors = Venue.validate("Nombre", "Dirección", "Ciudad", 1000, "")
        self.assertIn("contact", errors)
        self.assertEqual(errors["contact"], "Por favor ingrese un contacto")
