from django.urls import path
from . import views

urlpatterns = [
    path('stockgraph', views.search_stock_wrapper, name='stockgraph'),
    path('my-analysis/<int:analyst_id>/', views.my_analysis_page, name='my-analysis'),
]
