# templatetags/profile_tags.py
from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def user_link(user):
    if not getattr(user, "is_authenticated", False):
        name = getattr(user, "get_full_name", lambda: "")() or getattr(user, "username", "") or "Usuario"
        return name

    display = (user.get_full_name() or user.username or f"Usuario {user.pk}")
    username = (user.username or "").strip()

    try:
        if username:
            url = reverse("public_profile", kwargs={"username": username})
        else:
            # fallback por id si no tiene username
            url = reverse("public_profile_by_id", kwargs={"pk": user.pk})
        return format_html('<a href="{}">{}</a>', url, display)
    except Exception:
        return display
