from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from users.forms import LoginForm, RegisterForm, UpdateProfileForm, PasswordChangingForm, UserUpdateForm, ProfileForm
from django.contrib.auth.views import PasswordChangeView
from users.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def sign_up_view(request):
    if request.method == 'GET':
        user_form = RegisterForm()
        profile_form = ProfileForm()
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user_id = user
            profile.save()
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


def sign_in_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('show_details')

        messages.error(request, 'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


class PasswordsChangeView(PasswordChangeView, LoginRequiredMixin):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('login')


@login_required
def show_details(request):
    profile = Profile.objects.filter(user_id=request.user)[0]
    return render(request, 'users/profile_details.html', {'profile': profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('show_details')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit_profile.html', context)