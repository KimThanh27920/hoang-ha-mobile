from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ReadArticleSerializer
from ..models import Article
class ListArticleApiView(generics.ListAPIView):
    serializer_class = ReadArticleSerializer
    queryset = Article.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "tags__id", "tags__name"]

class RetrieveApiView(generics.RetrieveAPIView):
    serializer_class = ReadArticleSerializer
    queryset = Article.objects.filter(status=True)
    lookup_url_kwarg = "article_id"
