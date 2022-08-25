from django.urls import path
from . import views
urlpatterns = [
    path('',views.TransactionListAPI.as_view(), name="list-transactions"),
    
    
]