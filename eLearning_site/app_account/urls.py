from django.urls import path
from app_account import views

app_name = "app_account"

urlpatterns = [
    path('registration/', views.registrationView, name='registration'),
    path('login/', views.loginFormView, name='login'),
    path('logout/', views.logoutView, name="logout"),
    path('acc-info/', views.accountInformationView, name="accInfo"),
]