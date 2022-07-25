from itertools import product
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .serializers import VariantSerializer, VariantReadSerializer
from variants.models import Variant

from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime

class VariantViewSet(viewsets.ModelViewSet):
    serializer_class = {
        "list": VariantReadSerializer,
        "retrieve": VariantReadSerializer,
        "create": VariantSerializer,
        "update": VariantSerializer,
        "delete": VariantSerializer
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['product__name','color','version','front_cam','camera','pin','screen','storage','size','price','sale','network']
    filterset_fields = ['product__name','status','color','version','front_cam','camera','pin','screen','storage','size','price','sale','network']

    def get_serializer_class(self):
        return self.serializer_class[self.action]
    
    
    def get_queryset(self):
        if self.request.method == 'GET':
           return Variant.objects.all().select_related('product') 
        return Variant.objects.all()

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
        serializer = VariantSerializer(instance=instance, data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()