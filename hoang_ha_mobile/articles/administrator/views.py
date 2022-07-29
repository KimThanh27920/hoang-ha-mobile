from rest_framework.viewsets import ModelViewSet
from articles.models import Article
from articles.administrator.permissions import IsOwner
from articles.administrator.serializers import ArticleSerializer, ArticleRetrieveSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from datetime import datetime
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

FIELDS = [
            "id",
            "title",
            "description",
            "viewers",
            "status",
            "content",
            "created_at",
            "author__email",
            "author__phone",
            "updated_by__email",
            "updated_by__phone",
            "updated_at"
        ]
class ArticleViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = FIELDS
    search_fields = FIELDS
    filterset_fields = FIELDS
    

    def get_queryset(self):
        if self.action == "retrieve":
            return Article.objects.filter(deleted_by=None).prefetch_related("tags")
        return Article.objects.filter(deleted_by=None).select_related("author", "updated_by")

    def list(self, request, *args, **kwargs):
        is_paginate = bool(request.query_params.get(
            "paginate", False) == "true")
        if is_paginate:
            return super().list(request, *args, **kwargs)
        instances = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action != "update":
            return super().get_permissions()
        list_permission = super().get_permissions()
        is_owner = IsOwner()
        list_permission.append(is_owner)
        return list_permission

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleRetrieveSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user,
                        created_by=self.request.user, author=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.now()
        # TODO: @Bang: Why we need to update title here? We only need to check the deleted status of it.
        instance.title += "/" + str(instance.deleted_at)
        instance.deleted_by = self.request.user
        instance.save()
