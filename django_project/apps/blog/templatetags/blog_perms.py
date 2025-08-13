# apps/blog/templatetags/blog_perms.py
from django import template
from apps.blog.permissions import can_edit_comment, can_delete_comment
register = template.Library()

@register.simple_tag
def can_edit_com(user, com): return can_edit_comment(user, com)

@register.simple_tag
def can_delete_com(user, com): return can_delete_comment(user, com)

@register.simple_tag(takes_context=True)
def is_author_or_super(context):
    """
    True si el usuario está autenticado y:
    - pertenece al grupo 'autor', o
    - es superusuario
    """
    user = context["request"].user
    if not getattr(user, "is_authenticated", False):
        return False
    in_autor = user.groups.filter(name="Autor").exists()
    return in_autor or getattr(user, "is_superuser", False)