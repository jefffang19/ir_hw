from django import template

register = template.Library()

# value = {key : value}
# return value (a list)
def get_element(value, key):
    return value[key]

def remove_period(value):
    return value[:-1]

def check_empty(value):
    return len(value) == 0

def cal_percentage(value, div):
    return round(value/div * 100, 2)


register.filter('get_element', get_element)
register.filter('remove_period', remove_period)
register.filter('check_empty', check_empty)
register.filter('cal_percentage', cal_percentage)