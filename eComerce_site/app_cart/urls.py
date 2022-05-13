from unicodedata import name
from django.urls import path
from app_cart import views

app_name = "app_cart"

urlpatterns = [
    path('add/<int:pk>/', views.addToCartView, name="add"),
    path('cart/', views.cartView, name="cart"),
    path('remove/<int:pk>/', views.removeFromCartView, name="remove"),
    path('increase/<int:pk>/', views.increaseCartView, name="increase"),
    path('decrease/<int:pk>/', views.decreaseCartView, name="decrease"),
    path('coupon/', views.couponsView, name="coupon"),
    path('add-bronze/', views.addBronzeView, name="addBronze"),
    path('remove-bronze/', views.removeBronzeView, name="removeBronze"),
]
