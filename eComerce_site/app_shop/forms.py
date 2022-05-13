from django import forms
from app_shop.models import Product

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "product_category",
            "product_image",
            "product_name",
            "product_preview_text",
            "product_detial",
            "product_price",
            "product_quantity",
        )