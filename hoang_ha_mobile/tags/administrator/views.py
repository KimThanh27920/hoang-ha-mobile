from rest_framework.viewsets import ModelViewSet
from tags.models import Tag
from tags.administrator.serializers import TagSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, filters
from datetime import datetime

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all().prefetch_related()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = []
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user, created_by = self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by = self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.now()
        instance.deleted_by = self.request.user
        instance.save()
