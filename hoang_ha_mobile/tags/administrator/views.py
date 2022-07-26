from rest_framework.viewsets import ModelViewSet
from tags.models import Tag
from tags.administrator.serializers import TagSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, filters
from rest_framework.response import Response
from datetime import datetime


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.filter(deleted_by=None).prefetch_related()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user,
                        created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        is_paginate = bool(request.query_params.get(
            "paginate", False) == "true")
        if is_paginate:
            return super().list(request, *args, **kwargs)
        instances = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.now()
        instance.name += "/" + str(instance.deleted_at)
        instance.deleted_by = self.request.user
        instance.save()
