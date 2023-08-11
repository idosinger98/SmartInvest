from django.urls import path
from . import views

urlpatterns = [
    path('', views.community, name='community'),
    path('post-details/<int:post_id>/<int:profile_id>', views.show_post, name='post-details'),
    path('like_post/<int:post_id>/<int:profile_id>/', views.like_post, name='like_post'),
    path('post-details/<int:postId>/check-like/', views.check_like, name='check_like'),
    path('like_comment/<int:comment_id>/<int:profile_id>/', views.like_comment, name='like_comment'),
    path('post-details/<int:commentId>/check-comment-like/', views.check_comment_like, name='check_comment_like'),
    path('delete-comment/<int:post_id>/<int:comment_id>/<int:profile_id>/',
         views.delete_comment, name='delete_comment'),
    path("create-post/<int:pk>/", views.create_post_view, name='create_post'),
    # path("post-deatils/<int:pk>/", views.post_deatils, name="post_details"),
    # path("comment/<int:post_id>/", views.comment, name="comment"),
]
