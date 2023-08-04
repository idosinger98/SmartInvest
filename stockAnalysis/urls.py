from django.urls import path
from . import views

urlpatterns = [
    path('stockgraph', views.search_stock_view),
    path('indices', views.get_biggest_indices),
    path('algorithms', views.post_calculate_algorithms),
    path('stockAnalysisSave', views.save_stock_analysis),
]
