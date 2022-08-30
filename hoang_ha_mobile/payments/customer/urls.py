from django.urls import path
from . import views
urlpatterns = [
    path('stripe/checkout/',views.OrderAndCheckout.as_view(), name="confirm-payment-intent"),

    path('stripe/setup-intent/',views.SetupIntent.as_view(), name="setup-intent"),

    path('stripe/refund/',views.RefundAPI.as_view(), name="refund-request"),

]