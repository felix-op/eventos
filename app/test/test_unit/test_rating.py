from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Rating, Event
from django.utils import timezone

User = get_user_model()

class RatingTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="userPrueba", password="Password1")
        self.event = Event.objects.create(
            title="Titulo prueba event",
            description="Description prueba event",
            date=timezone.now()
        )
        
        self.rating = Rating.objects.create(
            user=self.user,
            event=self.event,
            title="Titulo prueba rating",
            text="Texto prueba rating",
            rating=2
        )

    def test_rating_creation(self):
        rating_prueba = Rating.objects.get(id=self.rating.id)

        self.assertEqual(rating_prueba.title, "Titulo prueba rating")
        self.assertEqual(rating_prueba.text, "Texto prueba rating")
        self.assertIsNotNone(rating_prueba.created_at)
        self.assertIsNotNone(rating_prueba.rating, 2)

        self.assertEqual(rating_prueba.user, self.user)
        self.assertEqual(rating_prueba.event, self.event)
    
    def test_rating_validate_with_valid_data(self):
        errors = Rating.validate(
            "Titulo prueba rating",
            "Texto prueba rating",
            3
        )
        self.assertEqual(errors, {})
    
    def test_rating_validate_with_none_title(self):
        title=None
        errors = Rating.validate(
            title,
            "Texto prueba rating",
            5
        )
        self.assertIn("title", errors)
        self.assertEqual(errors["title"], "El título no puede estar vacío")
    
    def test_rating_validate_with_superior_rating(self):
        rating=25
        errors = Rating.validate(
            "Titulo prueba rating",
            "Texto prueba rating",
            rating
        )
        self.assertIn("rating",errors)
        self.assertEqual(errors["rating"], "La calificación debe estar entre 1 y 5")
    
    def test_rating_validate_with_empty_text(self):
        text=""
        errors = Rating.validate(
            "Titulo prueba rating",
            text,
            2
        )
        self.assertIn("text",errors)
        self.assertEqual(errors["text"], "El texto no puede estar vacío")
    
    def test_rating_new_with_valid_data(self):
        initial_rating_count = Rating.objects.count()

        success, new_rating = Rating.new(
            user=self.user,
            event=self.event,
            title="Titulo prueba rating",
            text="Texto prueba rating",
            rating=5
        )

        self.assertTrue(success)
        self.assertIsInstance(new_rating, Rating, "El objeto devuelto debe ser una instancia de Rating.")
        self.assertEqual(Rating.objects.count(), initial_rating_count + 1)
        
        self.assertEqual(new_rating.user, self.user)
        self.assertEqual(new_rating.event, self.event)
        self.assertEqual(new_rating.rating, 5)
        self.assertEqual(new_rating.title, "Titulo prueba rating")
    
    def test_rating_new_with_invalid_data(self):
        inicial_rating_count = Rating.objects.count()
        rating = 250
        success, new_rating = Rating.new(
            user=self.user,
            event=self.event,
            title="",
            text="Texto prueba rating",
            rating=rating
        )

        self.assertFalse(success)
        self.assertNotIsInstance(new_rating, Rating, "El objeto rating no debería haberse creado")
        self.assertIn("title", new_rating, "Debería haber un error en el campo 'title'")
        self.assertIn("rating", new_rating, "Debería habber un error en el campo 'rating'")

        final_rating_count = Rating.objects.count()
        self.assertEqual(final_rating_count, inicial_rating_count,
                        "La cantidad de ratings en la DB no debería haber cambiado")
    
    def test_rating_update_with_valid_data(self):
        original_rating = Rating.objects.create(
            user=self.user,
            event=self.event,
            title="Titulo original prueba rating",
            text="Texto original prueba rating",
            rating=5
        )

        new_title="Titulo actualizado prueba rating"
        new_rating=3

        update_rating, errors = original_rating.update(title=new_title, rating=new_rating)

        self.assertTrue(update_rating, "La actualización debería ser exitosa")
        self.assertIsNone(errors, "No debería haber errores")

        original_rating.refresh_from_db()

        self.assertEqual(original_rating.title, new_title)
        self.assertEqual(original_rating.rating, new_rating)
        self.assertEqual(original_rating.text, "Texto original prueba rating")

    def test_rating_update_with_invalid_data(self):
        original_title="Titulo original prueba rating"
        original_rating=5

        obj_rating = Rating.objects.create(
            user=self.user,
            event=self.event,
            title=original_title,
            text="Texto original prueba rating",
            rating=original_rating
        )

        new_title=""
        new_rating=250

        update_rating, errors = obj_rating.update(title=new_title, rating=new_rating)

        self.assertFalse(update_rating, "La actualización debería haber fallado")
        self.assertIn("title", errors, "Debería haber un error en el campo 'title'")
        self.assertIn("rating", errors, "Debería haber un error en el campo 'rating'")

        obj_rating.refresh_from_db()

        self.assertEqual(obj_rating.title, original_title,
                            "No debería haber cambiado el titulo en la DB")
        self.assertEqual(obj_rating.rating, original_rating,
                            "No debería haber cambiado el ratign en la DB")