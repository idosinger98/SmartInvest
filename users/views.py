from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from users.forms import LoginForm


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
                return redirect('login')

        messages.error(request, 'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
