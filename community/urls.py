from django.urls import path
from . import views

urlpatterns = [
    path('', views.community, name='community'),
    path('post-details/<int:post_id>/<int:profile_id>', views.show_post, name='post-details'),
    path('like_post/<int:post_id>/<int:profile_id>/', views.like_post, name='like_post'),
    path('post-details/<int:postId>/check-like/', views.check_like, name='check_like'),
    path('like_comment/<int:comment_id>/<int:profile_id>/', views.like_comment, name='like_comment'),
    path('post-details/<int:commentId>/check-comment-like/', views.check_comment_like, name='check_comment_like'),
    path('delete-comment/<int:post_id>/<int:comment_id>/<int:profile_id>/', views.delete_comment, name='delete_comment'),
    path('fetch-posts', views.get_all_posts_as_json, name='fetch_posts'),
    path('create-new-post', views.create_new_post, name='create-new-post'),
    path("dashboard/<int:profile_id>/", views.dashboard, name="dashboard"),
]
