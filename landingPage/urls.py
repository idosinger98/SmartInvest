from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing_page'),
    path("contact/", views.contact, name="contact"),
]
