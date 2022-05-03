from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from app_account.forms import AccountInformationForm, AccountRegistrationForm
from app_account.models import AccountProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def registrationView(request):
    form = AccountRegistrationForm()
    registered = False

    if request.method == "POST":
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            profile_obj = AccountProfile()
            profile_obj.account = form.save()
            profile_obj.save()

            registered = True
            return HttpResponseRedirect(reverse('app_account:login'))
    
    dict = {
        "form": form,
        "title": "user registration",
        "registered": registered
    }
    return render(request, "app_account/user_registration.html", context=dict)

def loginFormView(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('app_account:accInfo'))
    dict = {
        'title': "User Login",
        "form": form,
    }
    return render(request, "app_account/user_login.html", context=dict)

@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('app_account:login'))

@login_required
def accountInformationView(request):
    current_user = AccountProfile.objects.get(account=request.user)
    
    form = AccountInformationForm(instance=current_user)
    if request.method == 'POST':
        form = AccountInformationForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = AccountInformationForm(instance=current_user)
            return HttpResponseRedirect(reverse('app_content:home'))

    user_str = str(current_user.account)
    dict = {
        'form':form,
        'title': user_str + "'s Profile",
        'loggedInUser': request.user,
    }
    return render(request, 'app_account/edit_profile.html', context=dict)