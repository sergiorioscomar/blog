# apps/core/management/commands/promover_autor.py
# python manage.py promover_autor serggiors
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Agrega el usuario al grupo Autor"

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, *args, **opts):
        User = get_user_model()
        u = User.objects.get(username=opts["username"])
        g = Group.objects.get(name="Autor")
        u.groups.add(g)
        self.stdout.write(self.style.SUCCESS(f"{u.username} ahora es Autor"))
