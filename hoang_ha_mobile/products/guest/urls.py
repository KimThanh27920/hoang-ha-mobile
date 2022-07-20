from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListProductyApiView.as_view()),
    path('<int:product_id>/', views.DetailProductApiView.as_view()),
    
]