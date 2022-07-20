from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CartOwnerAPIView.as_view(), name="list-item"),
]