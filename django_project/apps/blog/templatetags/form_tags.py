from django import template
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from apps.blog.widgets import SimpleSummernoteWidget 

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter
def is_summernote(field):
    return isinstance(field.field.widget, (SummernoteWidget, SummernoteInplaceWidget, SimpleSummernoteWidget))