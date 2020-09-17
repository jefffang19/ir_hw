from django import template

register = template.Library()

# value = {key : value}
# return value (a list)
def get_element(value, key):
    return value[key]


register.filter('get_element', get_element)