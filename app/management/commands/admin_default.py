from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = '⚠️ Crea un superusuario por defecto solo en modo DEBUG (desarrollo)'

    def handle(self, *args, **kwargs):
        # Verificación de entorno
        if not settings.DEBUG:
            raise CommandError("❌ Este comando solo puede ejecutarse con DEBUG = True (entorno de desarrollo)")

        self.stdout.write(self.style.WARNING("⚠️  Este comando está destinado solo para entornos de desarrollo o prueba."))
        self.stdout.write(self.style.WARNING("⚠️  NO usar en producción."))
        self.stdout.write("")

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS("👤 Ya existe un superusuario. No se crea uno nuevo."))
        else:
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS("✅ Superusuario creado: admin / admin123"))

        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("🛠 Puedes acceder al panel en: http://localhost:8000/admin/"))
