from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from users.models import Profile
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.contrib.auth.forms import PasswordResetForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class ProfileForm(forms.ModelForm):
    country = CountryField(blank_label='(Select country)').formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['phone_number', 'country', 'image']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Phone number already exists')
        return phone_number


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class UpdateProfileForm(forms.ModelForm):
    country = CountryField(blank_label='(Select country)').formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['phone_number', 'country', 'image']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Profile.objects.exclude(user_id=self.instance.user_id).filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone number already exists.')
        return phone_number


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='',
        help_text='Enter the email address associated with your account.'
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('There is no account associated with this email')
        return email
