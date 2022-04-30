from django.urls import path
from video_app import views

app_name = "app_video"

urlpatterns = [
    path('registration/', views.registrationView, name='registration'),
    path('login/', views.loginFormView, name='login'),
    path('logout/', views.logoutView, name="logout"),
    path('', views.homepageView, name="home"),
    path('upload/', views.uploadVideoView, name='upload'),
    path('video/<int:pk>', views.videoView, name='video')
]