# apps/blog/templatetags/blog_extras.py
from django import template
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import AnonymousUser

register = template.Library()

@register.simple_tag(takes_context=True)
def is_autor(context, obj):
    user = context["request"].user
    if not getattr(user, "is_authenticated", False):
        return False
    return getattr(obj, "autor", None) == user or getattr(user, "is_staff", False)
