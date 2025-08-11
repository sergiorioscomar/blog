# apps/core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apps.blog.models import Mensaje

User = get_user_model()

@receiver(post_save, sender=User)
def add_default_user_group(sender, instance, created, **kwargs):
    if created:
        g = Group.objects.filter(name="Usuario").first()
        if g:
            instance.groups.add(g)

@receiver(post_save, sender=Mensaje)
def email_nuevo_mensaje(sender, instance: Mensaje, created, **kwargs):
    if not created:
        return
    receptor = instance.receptor
    if not getattr(receptor, "email", None):
        return  # no hay dónde enviar

    path = reverse("detalle_mensaje", args=[instance.pk])
    site_url = getattr(settings, "SITE_URL", "")
    link = f"{site_url}{path}" if site_url else path

    ctx = {"mensaje": instance, "link": link}
    subject = f"Nuevo mensaje de {instance.emisor.username}"

    text_body = render_to_string("emails/new_message.txt", ctx)
    html_body = render_to_string("emails/new_message.html", ctx)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        to=[receptor.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=True)  # en prod: ponelo False si querés ver errores