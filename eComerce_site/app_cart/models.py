from django.db import models
from django.conf import settings
from app_shop.models import Product

# Create your models here.
class ShopCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cartUser")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartItem")
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        return format(self.item.product_price * self.quantity, '0.2f')

class ShopOrder(models.Model):
    orderitems = models.ManyToManyField(ShopCart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=264, blank=True, null=True)
    gold = models.IntegerField(default=0)
    bronze = models.IntegerField(default=0)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        total = total - (self.gold * 250)
        total = total - (self.bronze * 25)
        return total