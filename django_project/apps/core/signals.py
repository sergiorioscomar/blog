# apps/core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(post_save, sender=User)
def add_default_user_group(sender, instance, created, **kwargs):
    if created:
        g = Group.objects.filter(name="Usuario").first()
        if g:
            instance.groups.add(g)
