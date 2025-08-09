# apps/blog/templatetags/blog_extras.py
from django import template

register = template.Library()

@register.simple_tag
def is_autor(user):
    """Devuelve True si el usuario pertenece al grupo Autor."""
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name='Autor').exists()