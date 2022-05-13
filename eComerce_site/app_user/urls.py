from django.urls import path
from app_user import views

app_name = "app_user"

urlpatterns = [
    path('registration/', views.registrationView, name="registration"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('profile/', views.userProfileView, name="profile"),
]
