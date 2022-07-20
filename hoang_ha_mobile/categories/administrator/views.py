from rest_framework import filters,viewsets,permissions
from categories.administrator.serializers import CategorySerializer
from categories.models import Category
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        serializer.save(updated_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        data = {
            "name": instance.name,
            "deleted_by": self.request.user.id,
            "deleted_at": datetime.now()
        }
        serializer = CategorySerializer(instance=instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()