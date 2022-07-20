from rest_framework import generics
from .serializers import ReadProductSerializer
from ..models import Product
class ListProductyApiView(generics.ListAPIView):
    serializer_class = ReadProductSerializer
    queryset = Product.objects.filter(status=True)

class DetailProductApiView(generics.RetrieveAPIView):
    serializer_class = ReadProductSerializer
    queryset = Product.objects.filter(status=True)
    lookup_url_kwarg = 'product_id'