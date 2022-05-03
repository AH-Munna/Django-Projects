from django import forms
from app_content.models import ForumPost, PostAnswer, Quiz

class QuizForm(forms.ModelForm):
    quiz_date = forms.DateField(required=True, widget=forms.TextInput(attrs={'placeholder':"", "type": "date"}))
    class Meta:
        model = Quiz
        fields = ("quiz_title", "quiz_content", "quiz_date", "total_marks", )

        labels = {'quiz_content': "Quiz Questions"}

class CreateForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ("post_question", "post_desc", "post_image", )

        labels = {'post_image': "Image (optional)", "post_desc": "Description (optional)", "post_question": "Your Question"}

class AnswerForm(forms.ModelForm):
    class Meta:
        model = PostAnswer
        fields = ("answer", )