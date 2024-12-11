from django import template
import random

register = template.Library()

@register.filter
def random_color(value):
    """Genera un color hexadecimal aleatorio basado en el valor dado."""
    random.seed(value)  # Consistencia basada en el valor
    return f"#{random.randint(0, 0xFFFFFF):06x}"
