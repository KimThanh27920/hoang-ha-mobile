from rest_framework.viewsets import ModelViewSet
from tags.models import Tag
from tags.administrator.serializers import TagSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from datetime import datetime

FIELDS = [
            "id",
            "name",
            "status",
            "created_by__email",
            "created_by__phone",
            "created_at",
            "updated_by__email",
            "updated_by__phone",
            "updated_at"
        ]
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.filter(deleted_by=None).prefetch_related()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = FIELDS
    search_fields = FIELDS
    filterset_fields = FIELDS
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
