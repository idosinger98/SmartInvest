from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from users.forms import LoginForm, RegisterForm, ProfileForm


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
                return redirect('register')

        messages.error(request, 'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
