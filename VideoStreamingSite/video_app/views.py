from cmath import log
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from video_app.models import Video, Comment
from video_app.forms import CommentForm, UserRegistrationForm, VideoUploadForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def registrationView(request):
    form = UserRegistrationForm()
    registered = False

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            registered = True
            return HttpResponseRedirect(reverse('app_video:login'))

    return render(request, 'video_app/user_registration.html', context={'title': "New User", "form": form, "registered": registered})

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
                return HttpResponseRedirect(reverse('app_video:home'))
    return render(request, "video_app/user_login.html", context={'title': "User Login", "form": form})

@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('app_video:login'))

@login_required
def homepageView(request):
    all_videos = Video.objects.all

    if request.method == "GET":
        search = request.GET.get("search", '')
        search_result = Video.objects.filter(video_title__icontains=search)
        # search_result2 = User.objects.filter( first_name__icontains=search)
        # search_result3 = User.objects.filter( last_name__icontains=search)
        #search_result2 = UserProfile.objects.filter( full_name__icontains=search)
        #return HttpResponseRedirect(reverse('app_post:home'))

    dict = {
        "title": "Home Page",
        "video_list": all_videos,
        "search": search,
        "search_result": search_result
    }
    return render(request, 'index.html', context=dict)

def uploadVideoView(request):
    form = VideoUploadForm()

    if request.method == "POST":
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            video_obj = form.save(commit=False)
            video_obj.user = request.user
            video_obj.save()

            return HttpResponseRedirect(reverse('app_video:home'))

    return render(request, 'video_app/upload_video.html', context={'title':"upload video", 'form': form})

def videoView(request, pk):
    video = Video.objects.get(pk=pk)

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_obj = form.save(commit=False)
            comment_obj.user = request.user
            comment_obj.video = video
            comment_obj.save()
            return HttpResponseRedirect(reverse("app_video:video", kwargs={"pk": video.pk}))

    video.video_link = video.video_link.replace('width="560" height="315"', "width='100%' height='100%'")
    dict = {
        'title': video.video_title,
        'video': video,
        'form': form,
        'loggedInUser': request.user
    }
    return render(request, 'video_app/video_page.html', context=dict)