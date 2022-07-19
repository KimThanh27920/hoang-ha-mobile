from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from products.serializers import ProductSerializer
from products.models import Product

from datetime import datetime

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        data = {
            "name": instance.name,
            "deleted_by": self.request.user.id,
            "deleted_at": datetime.now()
        }
        serializer = ProductSerializer(instance=instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


