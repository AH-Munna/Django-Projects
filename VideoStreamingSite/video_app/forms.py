from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from video_app.models import Video, Comment

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, label="User Name", widget=forms.TextInput(attrs={'placeholder':"username....", "class": "mb-3"}))
    email = forms.EmailField(required=True, label="Email Address", widget=forms.TextInput(attrs={'placeholder':"email....", "class": "mb-3"}))
    password1 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(attrs={'placeholder':"password....", "class": "mb-3"}))
    password2 = forms.CharField(required=True, label="Enter Password again", widget=forms.PasswordInput(attrs={'placeholder':"re type password...."}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        #labels = {"username": "User Name", "password2": "Enter password again"}

class VideoUploadForm(forms.ModelForm):
    video_link = forms.CharField(required=True, label="Embeded video link", widget=forms.TextInput(attrs={'placeholder':"copy embeded link from video share option"}))
    video_title = forms.CharField(required=True, label="Title for your video", widget=forms.TextInput(attrs={'placeholder':"video title.........."}))
    class Meta:
        model = Video
        fields = ("video_category", "video_link", "video_title", "video_description", )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", )

        labels = {'comment': "Your opinion of the video"}