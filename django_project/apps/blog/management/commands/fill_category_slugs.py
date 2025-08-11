from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.blog.models import Categoria

class Command(BaseCommand):
    help = "Rellena slugs únicos de Categoria a partir del nombre."

    def handle(self, *args, **options):
        usados = set(c.slug for c in Categoria.objects.exclude(slug__isnull=True).exclude(slug=""))
        actualizados = 0
        for c in Categoria.objects.order_by("id"):
            base = slugify(c.nombre) or f"categoria-{c.id}"
            slug = c.slug or base
            if not slug or slug in usados and not Categoria.objects.filter(pk=c.pk, slug=slug).exists():
                i = 2
                cand = slug or base
                while cand in usados or Categoria.objects.filter(slug=cand).exclude(pk=c.pk).exists():
                    cand = f"{base}-{i}"
                    i += 1
                slug = cand
            if c.slug != slug:
                c.slug = slug
                c.save(update_fields=["slug"])
                actualizados += 1
            usados.add(c.slug)
        self.stdout.write(self.style.SUCCESS(f"Slugs actualizados: {actualizados}"))
