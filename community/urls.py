from django.urls import path
from community import views


urlpatterns = [
    path("community/", views.community, name="community"),
    path("create-post/<int:pk>/", views.create_post_view, name='create_post'),
]
