from rest_framework.viewsets import ModelViewSet
from articles.models import Article
from articles.administrator.serializers import ArticleSerializer, ArticleRetrieveSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, filters
from datetime import datetime
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().prefetch_related()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title","author__full_name","description","updated_by__full_name","deleted_by__full_name","created_at","updated_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleRetrieveSerializer
        return ArticleSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by = self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.now()
        instance.deleted_by = self.request.user
        instance.save()
