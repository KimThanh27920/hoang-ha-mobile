from rest_framework import filters, viewsets, permissions
from categories.administrator.serializers import CategorySerializer
from categories.models import Category
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Category.objects.filter(deleted_by=None)

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user,
                        created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        is_paginate = bool(request.query_params.get("paginate",False) == 'true')
        if is_paginate:
            return super().list(request, *args, **kwargs)
        instances = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
    
    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.deleted_at = datetime.now()
        instance.name += "/" + str(instance.deleted_at)
        instance.save()