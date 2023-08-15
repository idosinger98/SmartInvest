from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from users.forms import LoginForm, RegisterForm, UpdateProfileForm, PasswordChangingForm, UserUpdateForm, ProfileForm
from users.forms import ResetPasswordForm
from django.contrib.auth.views import PasswordChangeView
from users.models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from utils.email_utils import connectedApiAndSendEmail


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
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account
        user = request.user
        user.delete()

        # Logout the user
        logout(request)

        # Redirect to a success page or homepage
        return redirect('login')

    # Render the delete account confirmation template
    return render(request, 'users/change-password.html')


@login_required
def show_details(request):
    profile = Profile.objects.filter(user_id=request.user)[0]
    user_form = UserUpdateForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_details.html', context)


@login_required
def edit_profile(request):
    profile = Profile.objects.filter(user_id=request.user)[0]
    user_form = UserUpdateForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form
    }
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('show_details')
        else:
            context2 = {
                'profile': profile,
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'users/edit_profile.html', context2)

    return render(request, 'users/edit_profile.html', context)


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

            connectedApiAndSendEmail(subject_str, email, user)
            return render(request, message)

        else:
            messages.error(request, 'The email is not found in the system')
            return render(request, 'users/password_reset.html', {'form': form})
