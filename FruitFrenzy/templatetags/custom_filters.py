from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def float_multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return value

@register.filter
def float_add(value, arg):
    try:
        return float(value) + float(arg)
    except (TypeError, ValueError):
        return value
