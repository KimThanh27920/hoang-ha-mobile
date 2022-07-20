from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.CreateOrderAPIView.as_view(), name='create_order'),   
]