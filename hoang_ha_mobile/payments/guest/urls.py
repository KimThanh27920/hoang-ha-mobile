from django.urls import path
from . import views
urlpatterns = [
    path('stripe/setup-intent/',views.SetupIntent.as_view(), name="setup-intent"),
    path('stripe/confirm-setup-intent/',views.SetupIntentConfirmAPI.as_view(), name="confirm-setup-intent"),
]