from django import template

register = template.Library()

# value = {key : value}
# return value (a list)
def get_element(value, key):
    return value[key]

def remove_period(value):
    return value[:-1]


register.filter('get_element', get_element)
register.filter('remove_period', remove_period)