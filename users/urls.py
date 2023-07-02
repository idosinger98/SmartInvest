from django.urls import path
from . import views
from .views import PasswordsChangeView
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('login/', views.sign_in_view, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up_view, name='register'),
    path('password/', PasswordsChangeView.as_view(template_name='users/change-password.html'),
         name='change_password'),
    path('profile/details/', views.show_details, name='show_details'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password-reset/', views.reset_password, name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/reset_password_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
