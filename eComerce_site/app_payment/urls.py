from django.urls import path
from app_payment import views

app_name = "app_payment"

urlpatterns = [
    path("checkout/", views.billingView, name="checkout"),
    path("payment/", views.paymentView, name="payment"),
    path("pay-urls/", views.completeView, name="complete"),
    path("purchase/<val_id>/<tran_id>/", views.purchasedView, name="purchase"),
    path("purchase_list/", views.orderedView, name="purchased"),
]
