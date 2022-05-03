from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from app_account.models import AccountProfile
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from app_content.forms import AnswerForm, CreateForumPostForm, QuizForm
from app_content.models import Article, ForumPost, PostAnswer, Quiz

# Create your views here.
@login_required
def homepageView(request):
    user_type = AccountProfile.objects.get(account=request.user).account_type

    article_list = Article.objects.all()
    dict = {
        'title': "homepage",
        'user_type': user_type,
        "article_list": article_list,
    }
    return render(request, 'index.html', context=dict)

class ArticleView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'app_content/article_create.html'
    fields = ("article_title", "article_content", "article_img")

    def form_valid(self, form):
        user_type = AccountProfile.objects.get(account=self.request.user).account_type
        if user_type == "Student":
            return HttpResponseRedirect(reverse("app_content:home"))

        article_obj = form.save(commit=False)
        article_obj.teacher = self.request.user
        article_obj.article_slug = article_obj.article_title.replace(" ", "-") + "-" + str(uuid.uuid4())
        article_obj.save()
        return HttpResponseRedirect(reverse("app_content:home"))

@login_required
def QuizCreateView(request):
    form = QuizForm()
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz_obj = form.save(commit=False)
            quiz_obj.teacher = request.user
            quiz_obj.save()
            return HttpResponseRedirect(reverse("app_content:quizList"))

    dict = {
        "form": form,
        "title": "quiz create",
    }
    return render(request, "app_content/quiz_create.html", context=dict)

@login_required
def QuizListView(request):
    quiz_list = Quiz.objects.all()

    dict = {
        "quiz_list": quiz_list,
        "title": "All quizes",
    }
    return render(request, "app_content/quiz_list.html", context=dict)

@login_required
def createForumPostView(request):
    form = CreateForumPostForm()

    if request.method == "POST":
        form = CreateForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.author = request.user
            form_obj.save()
            return HttpResponseRedirect(reverse('app_content:forum'))

    dict = {
        "title": "ask a question in the forum",
        "form": form,
    }
    return render(request, "app_content/forum_post.html", context=dict)

@login_required
def forumView(request):
    forum_posts = ForumPost.objects.all()

    dict = {
        "title": "Forum Home",
        'forum_posts': forum_posts,
    }
    return render(request, "app_content/forum_home.html", context=dict)

def forumPostView(request, pk):
    post = ForumPost.objects.get(pk=pk)
    all_answers = PostAnswer.objects.filter(post=post)

    form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_obj = form.save(commit=False)
            answer_obj.post = post
            answer_obj.user = request.user
            answer_obj.save()
            return HttpResponseRedirect(reverse('app_content:post', kwargs={"pk": post.pk}))

    dict = {
        "post": post,
        "form": form,
        "title": post.post_question,
        "all_answers": all_answers,
        "loggedInUser": request.user
    }
    return render(request, "app_content/post.html", context=dict)