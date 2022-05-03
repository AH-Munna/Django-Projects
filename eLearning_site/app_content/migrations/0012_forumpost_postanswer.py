# Generated by Django 4.0.2 on 2022-05-03 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_content', '0011_alter_quiz_quiz_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_question', models.CharField(max_length=512)),
                ('post_desc', models.TextField(blank=True)),
                ('post_image', models.ImageField(blank=True, upload_to='')),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('post_update_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forumPostAuthor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-post_date',),
            },
        ),
        migrations.CreateModel(
            name='PostAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('answer_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forumPostComment', to='app_content.forumpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answerer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('answer_date',),
            },
        ),
    ]