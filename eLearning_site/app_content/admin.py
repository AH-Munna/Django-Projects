from django.contrib import admin
from app_content.models import Article, ForumPost, PostAnswer, Quiz

# Register your models here.
admin.site.register(Article)
admin.site.register(Quiz)
admin.site.register(ForumPost)
admin.site.register(PostAnswer)