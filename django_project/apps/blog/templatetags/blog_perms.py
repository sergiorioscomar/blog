# apps/blog/templatetags/blog_perms.py
from django import template
from apps.blog.permissions import can_edit_comment, can_delete_comment
register = template.Library()

@register.simple_tag
def can_edit_com(user, com): return can_edit_comment(user, com)

@register.simple_tag
def can_delete_com(user, com): return can_delete_comment(user, com)