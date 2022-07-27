# TODO: @all: check the Code Lay-out here. All spacing between classes, functions must be consistent. See guidelines: https://peps.python.org/pep-0008/. We need to refactor on all codes.
from rest_framework import generics
from .serializers import ReadCategorySerializer
from ..models import Category
class ListCategoryApiView(generics.ListAPIView):
    serializer_class = ReadCategorySerializer
    queryset = Category.objects.filter(status=True)
    pagination_class = None
