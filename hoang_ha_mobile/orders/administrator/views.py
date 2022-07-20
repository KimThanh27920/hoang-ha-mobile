from itertools import product
from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderDetailSerializer, OrderDetailReadSerializer
from orders.models import Order, OrderDetail

from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    #search_fields = ['product__id']
    filterset_fields = ['status','created_by']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        serializer.save(updated_by=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        data = {
            "id": instance.id,
            "deleted_by": self.request.user.id,
            "deleted_at": datetime.now()
        }
        serializer = OrderSerializer(instance=instance, data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

class OrderDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all().select_related('orders')
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    #search_fields = ['product__id']
    filterset_fields = ['order','variant','order__name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderDetailReadSerializer
        return OrderDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        serializer.save(updated_by=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        data = {
            "id": instance.id,
            "deleted_by": self.request.user.id,
            "deleted_at": datetime.now()
        }
        serializer = OrderDetailSerializer(instance=instance, data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

