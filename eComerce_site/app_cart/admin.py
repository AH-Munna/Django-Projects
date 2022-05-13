from django.contrib import admin
from app_cart.models import ShopCart, ShopOrder

# Register your models here.
admin.site.register(ShopCart)
admin.site.register(ShopOrder)