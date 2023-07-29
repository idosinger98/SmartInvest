from django.urls import path
from community import views


urlpatterns = [
    path("community/", views.community, name="community"),
    path("create-post/<int:pk>/", views.create_post_view, name='create_post'),
    path("post-deatils/<int:pk>/", views.post_deatils, name="post_deatils"),
    path("comment/<int:post_id>/", views.comment, name="comment"),
]
