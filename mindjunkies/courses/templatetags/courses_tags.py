import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter
def times(number):
    """Repeat given number of times."""
    return range(number)


@register.filter
def subtract(value, arg):
    return int(value) - int(arg)

@register.filter(name="add_class")
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})