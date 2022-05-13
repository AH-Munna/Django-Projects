from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from app_shop.forms import AddProductForm
from app_shop.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class Home(ListView):
    model = Product
    template_name = "index.html"

class ProductView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "app_shop/product_details.html"

@login_required
def addProductView(request):
    form = AddProductForm()
    current_user = request.user
    user_type = False
    if current_user.account_type == "Vendor":
        user_type = True


    if request.method == "POST" and user_type:
        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.product_vendor = current_user
            product_obj.save()
            return redirect("app_shop:home")
    elif current_user.account_type == "Buyer":
        messages.warning(request, "you are not a vendor. Can't add Products")
        return redirect("app_shop:home")
    
    dict = {
        "title": "New Product",
        "form": form,
    }
    return render(request, "app_shop/new_product.html", context=dict)