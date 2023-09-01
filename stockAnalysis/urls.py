from django.urls import path
from . import views

urlpatterns = [
    path('my-analysis/', views.my_analysis_page, name='my-analysis'),
    path('stockgraph', views.search_stock_view),
    path('indices', views.get_biggest_indices),
    path('algorithms', views.post_calculate_algorithms),
    path('stockAnalysisSave', views.save_stock_analysis),
    path('compareStocks/', views.compare_stocks),
    path("my-analysis-details/<int:pk>/", views.my_analysis_details_view, name='my_analysis_details'),
    path("edit-analysis-details/<int:pk>/", views.edit_analysis_details_view, name='edit_analysis_details'),
    path('delete-analysis/<int:pk>/', views.delete_analysis, name='delete_analysis'),
]
