from django.urls import path
from . import views

urlpatterns = [
    path('stockgraph', views.search_stock_view),
]
