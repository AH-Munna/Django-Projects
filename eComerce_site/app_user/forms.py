from django import forms
from app_user.models import User, UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user", "coupons_bronze", "coupons_gold")

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', "password2", "account_type")