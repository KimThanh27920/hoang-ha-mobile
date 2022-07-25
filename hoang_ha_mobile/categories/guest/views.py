from rest_framework import generics
from .serializers import ReadCategorySerializer
from ..models import Category
class ListCategoryApiView(generics.ListAPIView):
    serializer_class = ReadCategorySerializer
    queryset = Category.objects.filter(status=True)
    pagination_class = None
