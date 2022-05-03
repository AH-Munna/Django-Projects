from django import template

register = template.Library()

def range_filter_400(value):
    return value[0:500] + "............"

register.filter('range_filter_400', range_filter_400)