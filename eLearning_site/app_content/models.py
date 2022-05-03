from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Models for Teacher
class Article(models.Model):
    teacher = models.ForeignKey(User, related_name='article_teacher', on_delete=models.CASCADE)
    article_title = models.CharField(max_length=264, verbose_name='Article title')
    article_slug = models.SlugField(max_length=1024, unique=True)
    article_content = models.TextField(verbose_name="Article Content")
    article_img = models.ImageField(upload_to='article_images', verbose_name='Article image', blank=True)
    article_published_date = models.DateTimeField(auto_now_add=True)
    article_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-article_published_date',]

    def __str__(self) -> str:
        return self.article_title

class Quiz(models.Model):
    teacher = models.ForeignKey(User, related_name='quiz_teacher', on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=264, verbose_name="Quiz title")
    quiz_content = models.TextField()
    quiz_date = models.DateField()
    total_marks = models.IntegerField()

    class Meta:
        ordering = ['-quiz_date',]

class ForumPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forumPostAuthor")
    post_question = models.CharField(max_length=512)
    post_desc = models.TextField(blank=True)
    post_image = models.ImageField(blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    post_update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-post_date',)

    def __str__(self) -> str:
        return self.post_question

class PostAnswer(models.Model):
    post = models.ForeignKey(ForumPost, related_name='forumPostComment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= "answerer", on_delete=models.CASCADE)
    answer = models.TextField()
    answer_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('answer_date',)

    def __str__(self) -> str:
        return self.answer