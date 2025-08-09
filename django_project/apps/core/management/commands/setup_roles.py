# apps/core/management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.blog.models import Post, Comentario  # ajusta import/modelo de comentarios

class Command(BaseCommand):
    help = "Crea/actualiza grupos: Usuario y Autor"

    def handle(self, *args, **kwargs):
        # Permisos por modelo
        ct_post = ContentType.objects.get_for_model(Post)
        post_perms = {p.codename: p for p in Permission.objects.filter(content_type=ct_post)}

        ct_com = ContentType.objects.get_for_model(Comentario)
        com_perms = {p.codename: p for p in Permission.objects.filter(content_type=ct_com)}

        usuario, _ = Group.objects.get_or_create(name="Usuario")
        autor, _ = Group.objects.get_or_create(name="Autor")

        # Usuario: ver posts/comentarios + agregar comentario
        usuario.permissions.set([
            post_perms["view_post"],
            com_perms["view_comentario"],
            com_perms["add_comentario"],   # puede comentar
            # NO damos change/delete global de Comentario: eso será “sólo sus propios” por lógica
        ])

        # Autor: hereda lo de Usuario + crear post
        autor.permissions.set(list(usuario.permissions.all()) + [
            post_perms["add_post"],        # puede publicar
            # NO damos change/delete global de Post: será “sólo los suyos” por lógica
        ])

        self.stdout.write(self.style.SUCCESS("Roles Usuario y Autor configurados"))
