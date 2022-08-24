from django.urls import path
from . import views
urlpatterns = [

    
    path('stripe/refund/',views.RefundAPI.as_view(), name="refund"),
]