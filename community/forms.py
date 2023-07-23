from django import forms
from community.models import Post, Comment


class CreateCommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['content']


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Post
        fields = ['title', 'analysis_id']
