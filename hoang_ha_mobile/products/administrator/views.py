from rest_framework import viewsets,filters
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductSerializer, ProductReadSerializer
from products.models import Product

from datetime import datetime

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = {
        "list": ProductReadSerializer,
        "retrieve": ProductReadSerializer,
        "create": ProductSerializer,
        "update": ProductSerializer,
    }

    queryset = Product.objects.all().prefetch_related('variants').select_related('category')
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['category__name','variants__color','variants__version','product__name']
    filterset_fields = ['insurance','status','created_by','category__name','variants__color','variants__version']

    def get_serializer_class(self):
        return self.serializer_class[self.action]

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
            "name": instance.name,
            "deleted_by": self.request.user.id,
            "deleted_at": datetime.now()
        }
        serializer = ProductSerializer(instance=instance, data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


