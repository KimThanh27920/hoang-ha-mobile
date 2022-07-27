from ast import Delete
from multiprocessing import set_forkserver_preload
from unicodedata import category
from rest_framework import generics
from .serializers import ReadProductSerializer, ReadDetailProductSerializer
from ..models import Product
from variants.models import Variant


class ListProductyApiView(generics.ListAPIView):
    serializer_class = ReadProductSerializer
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(status=True, deleted_by=None, category=self.request.query_params.get('category')).select_related('category')


class DetailProductApiView(generics.RetrieveAPIView):
    serializer_class = ReadDetailProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg = 'product_id'

