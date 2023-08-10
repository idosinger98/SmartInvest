from django.urls import path
from community import views


urlpatterns = [
    path("community/", views.community, name="community"),
]
