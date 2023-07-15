from django.urls import path
from . import views

urlpatterns = [
    path('', views.community, name='community'),
    path('post-details/<int:pk>/', views.show_post, name='post-details'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
]
