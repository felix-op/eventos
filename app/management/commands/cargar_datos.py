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

            call_command('loaddata', 'user_groups.json')
            self.stdout.write(self.style.SUCCESS("Grupos de usuarios cargados ✅"))

            call_command('loaddata', 'client_users.json')
            self.stdout.write(self.style.SUCCESS("Usuarios clientes, cargados ✅"))

            call_command('loaddata', 'tickets.json')
            self.stdout.write(self.style.SUCCESS("tickets cargados ✅"))

            call_command('loaddata', 'comments.json')
            self.stdout.write(self.style.SUCCESS("comments cargados ✅"))

            call_command('loaddata', 'notifications.json')
            self.stdout.write(self.style.SUCCESS("notifications cargados ✅"))

            call_command('loaddata', 'notifications_user.json')
            self.stdout.write(self.style.SUCCESS("notifications_user cargados ✅"))

        except Exception as e:
            raise CommandError(f"Ocurrió un error al cargar fixtures: {e}")
    