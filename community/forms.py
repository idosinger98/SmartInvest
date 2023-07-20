from django import forms
from community.models import Post, Comment


class CreateCommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = ['content']

    # def clean_content(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
    #         raise forms.ValidationError('This email address is already in use.')
    #     return email
