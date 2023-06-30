from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createReviewView, name='create_review'),
]
