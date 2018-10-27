from django import template
from django.utils.safestring import mark_safe
register=template.Library()

@register.simple_tag
def a(a1,a2):
    return a1+a2
@register.filter
def b(a1,a2):
    return a1+a2