from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploader", default='1')

    CATEGORY_CHOICES = [
        ('ALL', 'All category'),
        ('SCIENCE', 'Science'),
        ('GAMING', 'Gaming'),
        ('MOVIES', 'Movies'),
    ]
    video_category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, default='ALL')

    video_link = models.CharField(max_length=2048)
    video_title = models.CharField(max_length=264, default='title')
    video_upload_date = models.DateTimeField(auto_now_add=True)
    video_description = models.TextField(blank=True)

    class Meta:
        ordering = ('-video_upload_date',)

class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='video_comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= "commenter", on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('comment_date',)

    def __str__(self) -> str:
        return self.comment