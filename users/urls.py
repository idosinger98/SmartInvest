from django.urls import path
from . import views
from .views import PasswordsChangeView

urlpatterns = [
    path('login/', views.sign_in_view, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up_view, name='register'),
    path('password/', PasswordsChangeView.as_view(template_name='users/change-password.html'),
         name='change_password'),
    path('profile/details/', views.show_details, name='show_details'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
