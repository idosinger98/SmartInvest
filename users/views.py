from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, ResetPasswordForm
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.http import BadHeaderError
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db.models.query_utils import Q


def sign_in(request):
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
                # I'll change it when we have the proper page
                return redirect('login')

        messages.error(request, 'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def reset_password(request):
    if request.method == 'GET':
        form = ResetPasswordForm()
        return render(request, 'users/password_reset.html', {'form': form})

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            return send_email(request, email, "Password Reset Requested", 'users/password_reset_email.html',
                              'users/reset_password_done.html', False, form)
        else:
            # Handle form validation errors
            return render(request, 'users/password_reset.html', {'form': form})


def send_email(request, email, subject_str, email_template_html, message, flag, form):
    associated_users = User.objects.filter(Q(email=email))
    for user in associated_users:
        if user.is_active or flag:
            subject = subject_str
            email_template_name = email_template_html
            c = {
                "email": user.email,
                'domain': '127.0.0.1:8000',
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'smartinvest850@gmail.com', [user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, message)

        else:
            messages.error(request, 'The email is not found in the system')
            return render(request, 'users/password_reset.html', {'form': form})
