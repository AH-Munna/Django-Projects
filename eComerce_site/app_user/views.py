from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# forms and models
from app_user.models import UserProfile
from app_user.forms import RegistrationForm, UserProfileForm

# Create your views here.
def registrationView(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return HttpResponseRedirect(reverse("app_user:login"))

    dict = {
        "form": form,
        "title": "registration page",
    }
    return render(request, "app_user/registration.html", context=dict)

def loginView(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                print('user is ', user)
                login(request, user)
                messages.success(request, "Logged in successfully")
                return HttpResponseRedirect(reverse("app_user:profile"))

    dict = {
        'form': form,
        "title": "login page",
    }
    return render(request, "app_user/user_login.html", context=dict)

@login_required
def logoutView(request):
    logout(request)
    messages.warning(request, "Logged out")
    return HttpResponseRedirect(reverse("app_user:login"))

@login_required
def userProfileView(request):
    profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=profile)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated")
            form = UserProfileForm(instance=profile)
    
    if profile.username == "":
        loggedInUser = "user"
    else:
        loggedInUser = profile.username
    dict = {
        "form": form,
        "loggedInUser": loggedInUser,
    }
    return render(request, "app_user/user_profile.html", context=dict)