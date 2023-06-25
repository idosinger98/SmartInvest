from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.sign_in_view, name='login'),
    path('logout/', views.sign_out, name='logout'),
]