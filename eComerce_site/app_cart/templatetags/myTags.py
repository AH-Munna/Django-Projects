from atexit import register
from django import template
from app_cart.models import ShopOrder

register = template.Library()

@register.filter
def cart_total(user):
    order = ShopOrder.objects.filter(user=user, ordered=False)

    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0