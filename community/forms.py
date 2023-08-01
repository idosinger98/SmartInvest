from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['content']
