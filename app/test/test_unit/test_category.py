from django.test import TestCase
from app.models import Category

class TestCategoryCreation(TestCase):
    def test_create_category_valid(self):
        success, category = Category.new(
            name="Deporte",
            description="Eventos deportivos",
            is_active=True
        )
        self.assertTrue(success)
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, "Deporte")
        self.assertEqual(category.description, "Eventos deportivos")
        self.assertTrue(category.is_active)
    
    def test_create_category_invalid_empty_name_and_description(self):
        success, errors = Category.new(name="", description="")
        self.assertFalse(success)
        self.assertIn("name", errors)
        self.assertIn("description", errors)

    def test_create_category_invalid_whitespace(self):
        success, errors = Category.new(name="   ", description="   ")
        self.assertFalse(success)
        self.assertIn("name", errors)
        self.assertIn("description", errors)

class TestCategoryValidation(TestCase):
    def test_validate_category_with_empty_name(self):
        errors = Category.validate(name="", description="Una Descripción")
        self.assertIn("name", errors)
        self.assertNotIn("description", errors)

    def test_validate_category_with_empty_description(self):
        errors = Category.validate(name="Un Nombre", description="")
        self.assertIn("description", errors)
        self.assertNotIn("name", errors)

    def test_validate_category_with_empty_name_and_description(self):
        errors = Category.validate(name="", description="")
        self.assertIn("name", errors)
        self.assertIn("description", errors)

    def test_validate_category_with_valid_data(self):
        errors = Category.validate(name="Educación", description="Eventos educativos")
        self.assertEqual(errors, {})

class TestCategoryUpdate(TestCase):
    def setUp(self):
        _, self.category = Category.new(
            name="Arte",
            description="Eventos artísticos",
            is_active=False
        )

    def test_update_category_name(self):
        self.category.update(name="Artes Visuales")
        updated = Category.objects.get(pk=self.category.pk)
        self.assertEqual(updated.name, "Artes Visuales")
        self.assertEqual(updated.description, "Eventos artísticos")
        self.assertFalse(updated.is_active)

    def test_update_category_description(self):
        self.category.update(description="Exposiciones y museos")
        updated = Category.objects.get(pk=self.category.pk)
        self.assertEqual(updated.description, "Exposiciones y museos")
        self.assertEqual(updated.name, "Arte")
        self.assertFalse(updated.is_active)

    def test_update_category_is_active(self):
        self.category.update(is_active=True)
        updated = Category.objects.get(pk=self.category.pk)
        self.assertTrue(updated.is_active)
        self.assertEqual(updated.name, "Arte")
        self.assertEqual(updated.description, "Eventos artísticos")

    def test_update_category_no_changes(self):
        self.category.update()
        updated = Category.objects.get(pk=self.category.pk)
        self.assertEqual(updated.name, "Arte")
        self.assertEqual(updated.description, "Eventos artísticos")
        self.assertFalse(updated.is_active)