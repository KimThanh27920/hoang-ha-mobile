from django.urls import path, include
from .views import OrderViewSet,OrderDetailViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("order-detail", OrderDetailViewSet, basename="order_detail")
router.register("", OrderViewSet, basename="order")

urlpatterns = [
    path('', include(router.urls))
]