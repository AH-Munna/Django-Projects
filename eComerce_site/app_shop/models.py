from app_user.models import User
from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "ProductCategories"

class Product(models.Model):
    product_vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendor")
    product_image = models.ImageField(upload_to="product_image")
    product_name = models.CharField(max_length=264)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="product_category")
    product_preview_text = models.TextField(max_length=300, verbose_name="Preview Text")
    product_detial = models.TextField(max_length=1024, verbose_name="Product Description")
    product_price = models.FloatField()
    product_quantity = models.IntegerField()
    old_price = models.FloatField(default=0.00)
    product_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ["-product_added",]