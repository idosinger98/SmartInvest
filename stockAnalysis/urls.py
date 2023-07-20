from django.urls import path
from . import views

urlpatterns = [
    path('stockgraph', views.search_stock_view),
    path('indices', views.get_biggest_indices),
]
