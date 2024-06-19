from django import template

register = template.Library()

@register.filter
def dict_key(value, key):
    return value.get(key)
