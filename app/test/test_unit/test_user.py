from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import User

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_creation(self):
        #Test que verifica la creación correcta de un usuario
        user = User.objects.create_user(username='usuario_prueba', password='contraseña123')
        self.assertEqual(user.username, 'usuario_prueba')
        self.assertTrue(user.check_password('contraseña123'))

    def test_str_method_returns_username(self):
        #Test que verifica que el método __str__ funcione correctamente
        user = User.objects.create_user(username='usuario_test', password='test123')
        self.assertEqual(str(user), 'usuario_test')

    def test_update_with_new_username(self):
        #Test que verifica la actualización del username mediante el método update
        user = User.objects.create_user(username='viejo_nombre', password='12345')
        user.update(username='nuevo_nombre')

        # Recargar desde la base de datos
        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.username, 'nuevo_nombre')

    def test_update_without_arguments_does_nothing(self):
        #Test que verifica que el método update sin argumentos no modifica el usuario
        user = User.objects.create_user(username='nombre_original', password='abc123')
        user.update()  # Sin argumentos

        # Recargar desde la base de datos
        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.username, 'nombre_original')
