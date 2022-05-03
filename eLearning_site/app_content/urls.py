from django.urls import path
from app_content import views

app_name = "app_content"

urlpatterns = [
    path('', views.homepageView, name="home"),
    path('create-article/', views.ArticleView.as_view(), name="createArticle"),
    path('create-quiz/', views.QuizCreateView, name="createQuiz"),
    path('quiz-list/', views.QuizListView, name="quizList"),
    path('form-post/', views.createForumPostView, name='forumPost'),
    path('forum/', views.forumView, name="forum"),
    path('post/<int:pk>', views.forumPostView, name="post"),
]