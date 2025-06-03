from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Carga fixtures en orden: categorías, venues y eventos'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.NOTICE("Cargando fixtures..."))

            call_command('loaddata', 'categories.json')
            self.stdout.write(self.style.SUCCESS("Categorías cargadas ✅"))

            call_command('loaddata', 'venues.json')
            self.stdout.write(self.style.SUCCESS("Venues cargados ✅"))

            call_command('loaddata', 'events.json')
            self.stdout.write(self.style.SUCCESS("Eventos cargados ✅"))

            call_command('loaddata', 'notifications.json')
            self.stdout.write(self.style.SUCCESS("Loaded Notifications ✅"))

            call_command('loaddata', 'user_groups.json')
            self.stdout.write(self.style.SUCCESS("Grupos de usuarios cargados ✅"))

        except Exception as e:
            raise CommandError(f"Ocurrió un error al cargar fixtures: {e}")
    