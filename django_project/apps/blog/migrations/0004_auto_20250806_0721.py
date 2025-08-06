# Crear categorias iniciales


from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    initial_categories = ['soporte', 'redes', 'ciberseguridad','seguridad','desarrollo','desarrollo-web','diseño-web','marketing-digital','redes-sociales']
    for cat in initial_categories:
        Category.objects.get_or_create(nombre=cat)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]
