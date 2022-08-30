from django.urls import path
from . import views
urlpatterns = [
    path('checkout/', views.OrderAndCheckout.as_view()),
    path('get_pm/', views.CreatePaymentMethod.as_view()),
]