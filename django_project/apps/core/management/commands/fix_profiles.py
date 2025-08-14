from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.tu_app_perfiles.models import Profile  # ajusta al nombre real de tu app

class Command(BaseCommand):
    help = "Crea perfiles que falten para usuarios existentes (por ejemplo, admin antiguos)."

    def handle(self, *args, **options):
        User = get_user_model()
        creados = 0

        for u in User.objects.all():
            _, was_created = Profile.objects.get_or_create(user=u)
            if was_created:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f"Perfiles creados: {creados}"))
