from django import template

register = template.Library()


@register.filter(name='total_price')
def total_price(first_value, second_value):
    return first_value * second_value