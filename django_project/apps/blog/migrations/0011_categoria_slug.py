from django.db import migrations, models
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    Categoria = apps.get_model('blog', 'Categoria')

    def unique_slug(instance, base):
        base = slugify(base) or f"categoria-{instance.pk or ''}".strip('-')
        slug = base
        i = 2
        while Categoria.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    for c in Categoria.objects.all().order_by('id'):
        if not c.slug:
            c.slug = unique_slug(c, c.nombre)
            c.save(update_fields=['slug'])

class Migration(migrations.Migration):

    # 👇 MUY IMPORTANTE: que dependa de 0010_post_views
    dependencies = [
        ('blog', '0010_post_views'),
    ]

    operations = [
        # 1) Agregar slug como NULLABLE (no rompe)
        migrations.AddField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(max_length=90, null=True, blank=True, db_index=True),
        ),
        # 2) Poblar slugs desde nombre (garantiza unicidad)
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        # 3) Endurecer: hacerlo único (y NOT NULL implícito)
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(max_length=90, unique=True, db_index=True),
        ),
    ]

