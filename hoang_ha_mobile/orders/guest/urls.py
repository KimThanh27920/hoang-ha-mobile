from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.CreateOrderApiView.as_view()),
    path('<int:order_id>/', views.OrderDetailApiView.as_view()),

    path('checkout/', views.OrderAndCheckout.as_view()),
    path('get_pm/', views.CreatePaymentMethod.as_view()),
]