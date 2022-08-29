from django.urls import path
from . import views
urlpatterns = [
    path('stripe/create-payment-intent/',views.PaymentIntentCreateAPI.as_view(), name="create-payment-intent"),
    path('stripe/checkout/',views.PaymentIntentConfirmAPI.as_view(), name="confirm-payment-intent"),

    path('stripe/setup-intent/',views.SetupIntent.as_view(), name="setup-intent"),
    path('stripe/confirm-setup-intent/',views.SetupIntentConfirmAPI.as_view(), name="confirm-setup-intent"),

    path('stripe/refund/',views.RefundAPI.as_view(), name="refund-request"),

]