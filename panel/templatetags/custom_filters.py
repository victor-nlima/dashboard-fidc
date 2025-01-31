from django import template
import locale

register = template.Library()

@register.filter
def format_brl(value):
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format_string('%.2f', float(value), grouping=True)
    except ValueError:
        return value
