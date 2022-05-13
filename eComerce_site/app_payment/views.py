import profile
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from app_payment.forms import BillingForm
from app_payment.models import BillingAddress
from app_cart.models import ShopCart, ShopOrder
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# payments
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import requests
import socket

# Create your views here.
@login_required
def billingView(request):
    user_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    form = BillingForm(instance=user_address)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=user_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=user_address)
            messages.success(request, f"Shipping Address updated")
            return redirect("app_payment:checkout")

    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)[0]
    order_items = order_obj.orderitems.all()
    order_total = order_obj.get_totals()

    dict = {
        "title": "Checkout",
        "form": form,
        "order_total": order_total,
        "user_address": user_address,
        "order_items": order_items,
    }
    return render(request, "app_payment/checkout.html", context=dict)

@login_required
def paymentView(request):
    customer = request.user
    user_address = BillingAddress.objects.get_or_create(user=request.user)[0]

    if not user_address.is_fully_filled():
        messages.info(request, f"Please fill up all fields in Shipping Address")
        return redirect("app_payment:checkout")
    
    if not customer.userProfile.is_fully_filled():
        messages.info(request, f"Please complete profile details")
        return redirect("app_user:profile")

    # payment id and api
    store_id = 'abc6278d9df380c4'
    API_key = 'abc6278d9df380c4@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)
    
    # payment urls
    pay_url = request.build_absolute_uri(reverse("app_payment:complete"))
    mypayment.set_urls(success_url=pay_url, fail_url=pay_url, cancel_url=pay_url, ipn_url=pay_url)
    
    # payment product detials
    order_obj = ShopOrder.objects.filter(user=customer, ordered=False)[0]
    order_items = order_obj.orderitems.all()
    order_item_count = order_obj.orderitems.count()
    order_total = order_obj.get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_item_count, shipping_method='Courier', product_profile='None')
    
    # customer
    mypayment.set_customer_info(name=customer.userProfile.full_name, email=customer.email, address1=customer.userProfile.address, address2=customer.userProfile.address, city=customer.userProfile.city, postcode=customer.userProfile.zipcode, country=customer.userProfile.country, phone=customer.userProfile.phone)
    mypayment.set_shipping_info(shipping_to=customer.userProfile.full_name, address=user_address.address, city=user_address.city, postcode=user_address.zipcode, country=user_address.country)

    response_data = mypayment.init_payment()
    print(response_data)

    dict = {
        "title": "payment",
    }
    #return render(request, "app_payment/payment.html", context=dict)
    return redirect(response_data["GatewayPageURL"])

@csrf_exempt
def completeView(request):
    if request.method == "POST" or request.method == "post":
        payment_data = request.POST
        payment_status = payment_data["status"]
        transaction_id = payment_data["tran_id"]
        bank_transaction_id = payment_data["bank_tran_id"]

        if payment_status == "VALID":
            messages.success(request, f"Your payment complted successfully. You will be redirected to home in 5 seconds")
            validation_id = payment_data["val_id"]
            return HttpResponseRedirect(reverse("app_payment:purchase", kwargs={"val_id": validation_id, "tran_id": transaction_id}))
        elif payment_status == "FAILED":
            payment_error = payment_data["error"]
            messages.warning(request, f"{payment_error}. Payment failed. You can try again.")

    dict = {
        "title": "payment urls"
    }
    return render(request, "app_payment/complete.html", context=dict)

@login_required
def purchasedView(request, val_id, tran_id):
    try:
        order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)[0]
    except:
        messages.warning(request, "no item in cart.")
        return redirect("app_shop:home")
    order_obj.ordered = True
    order_obj.orderId = val_id
    order_obj.payment_id = tran_id
    order_obj.save()

    total_money = order_obj.get_totals()
    profile = request.user.userProfile
    if total_money >= 10000:
        profile.coupons_gold += int(total_money/10000)
        profile.coupons_bronze += int( (total_money%10000) / 1000)
        profile.save()
    elif total_money >= 1000:
        profile.coupons_bronze += int(total_money/1000)
        profile.save()
        

    cart_item = ShopCart.objects.filter(user=request.user, purchased=False)
    for item in cart_item:
        item.purchased = True
        item.save()
        
    dict = {
        "title": "payment urls",
    }
    return render(request, "app_payment/complete.html", context=dict)

@login_required
def orderedView(request):
    try:
        orders = ShopOrder.objects.filter(user=request.user, ordered=True)
        dict = {
            "title": "Purchased items",
            "orders": orders,
        }
    except:
        messages.warning(request, "You have no purchased item")
        return redirect("app_shop:home")
    
    return render(request, "app_payment/purchase_list.html", context=dict)