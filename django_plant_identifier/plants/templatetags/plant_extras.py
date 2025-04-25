from django import template

register = template.Library()

@register.filter
def trim(value):
    """Trims whitespace from the beginning and end of a string."""
    if value:
        return value.strip()
    return value
