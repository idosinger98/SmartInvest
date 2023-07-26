from django import forms
from community.models import Comment


class CreateCommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['content']
