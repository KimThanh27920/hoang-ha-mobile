from rest_framework.viewsets import ModelViewSet
from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
