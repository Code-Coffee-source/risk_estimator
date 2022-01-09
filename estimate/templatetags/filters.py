from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='titleify')
def addclass(value):
    try:
        return value.replace("_", " ").title()
    except AttributeError:
        return value
