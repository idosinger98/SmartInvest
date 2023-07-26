from django import forms
from community.models import Post, Comment


class CreateCommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['content']
