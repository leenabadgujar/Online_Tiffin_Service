from django import template

register = template.Library()


@register.filter(name='check')
def check(value,check_value):
    if value == check_value:
        return True