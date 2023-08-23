from django.urls import path
from . import views

urlpatterns = [
    path('create-review/', views.create_review_view, name='create_review'),
    path('delete-review/', views.delete_review, name='delete_review'),
]
