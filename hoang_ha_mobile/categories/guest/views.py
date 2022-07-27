from rest_framework import generics, views, response

from .serializers import ReadCategorySerializer, ReadDetailCategorySerializer
from ..models import Category

from variants.guest.serializers import ReadVarianSerializer
from variants.models import Variant



class ListCategoryApiView(generics.ListAPIView):
    serializer_class = ReadCategorySerializer
    queryset = Category.objects.filter(status=True)
    pagination_class = None


class DetailCategoryApiView(generics.ListAPIView):
    serializer_class = ReadDetailCategorySerializer

    def get_queryset(self):
        return Variant.objects.filter(deleted_by = None, status=True, product__category = self.kwargs.get('category_id'))
