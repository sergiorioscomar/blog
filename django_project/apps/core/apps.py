from django.apps import AppConfig

def ready(self):
    from . import signals


class MensajesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core"

    def ready(self):
        from . import signals