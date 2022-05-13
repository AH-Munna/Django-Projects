from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app_cart.models import ShopCart, ShopOrder
from app_shop.models import Product

# Create your views here.
@login_required
def addToCartView(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = ShopCart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)

    if order_obj.exists():
        order = order_obj[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "Quantity of this item has been updated")
            return redirect("app_shop:home")
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "Item added to Cart.")
            return redirect("app_shop:home")
    else:
        order = ShopOrder(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "Item added to Cart.")
        return redirect("app_shop:home")

@login_required
def cartView(request):
    carts = ShopCart.objects.filter(user=request.user, purchased=False)
    orders = ShopOrder.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]

        dict = {
            "title": "Cart items",
            "carts": carts,
            "order": order,
            "gold": request.user.userProfile.coupons_gold,
            "bronze": request.user.userProfile.coupons_bronze,
        }
        return render(request, "app_cart/cart.html", context=dict)
    else:
        messages.warning(request, "You haven't added any item to cart")
        return redirect("app_shop:home")

@login_required
def removeFromCartView(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)
    if order_obj.exists():
        order = order_obj[0]
        if order.orderitems.filter(item=item).exists():
            order_item = ShopCart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "item removed from cart")
            return redirect("app_cart:cart")
        else:
            messages.info(request, "no such item")
            return redirect("app_shop:home")
    else:
        messages.info(request, "no such item")
        return redirect("app_shop:home")

@login_required
def increaseCartView(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)
    if order_obj.exists():
        order = order_obj[0]
        if order.orderitems.filter(item=item).exists():
            order_item = ShopCart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 0:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.product_name}'s quantity increased")
                return redirect("app_cart:cart")
        else:
            messages.info(request, f"{item.product_name} is not in your cart")
            return redirect("app_shop:home")
    else:
        messages.info(request, "no such item")
        return redirect('app_shop:home')

@login_required
def decreaseCartView(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)
    if order_obj.exists():
        order = order_obj[0]
        if order.orderitems.filter(item=item).exists():
            order_item = ShopCart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.product_name}'s quantity decreased")
                return redirect("app_cart:cart")
            else:
                return HttpResponseRedirect(reverse("app_cart:remove", kwargs={"pk":order_item.item.pk}))
                #return redirect("app_cart:remove", kwargs={"pk":order_item.item.pk})
        else:
            messages.info(request, f"{item.product_name} is not in your cart")
            return redirect("app_shop:home")
    else:
        messages.info(request, "no such item")
        return redirect('app_shop:home')

@login_required
def couponsView(request):
    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)[0]
    total_money = order_obj.get_totals()
    gold = request.user.userProfile.coupons_gold
    bronze = request.user.userProfile.coupons_bronze

    dict = {
        "title": "Use Coupons",
        "total": total_money,
        "gold": gold,
        "bronze": bronze,
        "usedBronze": ShopOrder.objects.filter(user=request.user, ordered=False)[0].bronze,
        "usedGold": ShopOrder.objects.filter(user=request.user, ordered=False)[0].gold,
    }
    return render(request, "app_cart/coupon.html", context=dict)

@login_required
def addGoldView(request):
    gold = request.user.userProfile.coupons_gold
    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)[0]
    total_money = order_obj.get_totals()

@login_required
def addBronzeView(request):
    profile = request.user.userProfile
    profile.coupons_bronze -= 1
    profile.save()

    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)[0]
    order_obj.bronze += 1
    order_obj.save()

    return redirect("app_cart:coupon")
    
@login_required
def removeBronzeView(request):
    profile = request.user.userProfile
    profile.coupons_bronze += 1
    profile.save()

    order_obj = ShopOrder.objects.filter(user=request.user, ordered=False)[0]
    order_obj.bronze -= 1
    order_obj.save()

    return redirect("app_cart:coupon")

    



