from django.urls import path
from . import views
urlpatterns = [
    path('stripe/create-payment-intent/',views.PaymentIntentCreateAPI.as_view(), name="create-payment-intent"),
    path('stripe/checkout/',views.PaymentIntentConfirmAPI.as_view(), name="confirm-payment-intent"),
    
]