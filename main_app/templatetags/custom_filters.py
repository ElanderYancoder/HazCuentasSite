# main_app/templatetags/custom_filters.py
import random
from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Resta `arg` de `value`, manejando solo números."""
    try:
        return float(value) - float(arg)  # Convertir a float para evitar errores de tipo
    except (ValueError, TypeError):
        # Devuelve `value` sin modificar si no se puede hacer la resta
        return value
    
    

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Añade una clase CSS al campo de un formulario."""
    return field.as_widget(attrs={"class": css_class})



# filtor 
from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """Añadir una clase CSS a un campo de formulario"""
    return value.as_widget(attrs={"class": arg})







