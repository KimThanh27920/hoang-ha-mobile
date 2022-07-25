
from itertools import product
from rest_framework import generics, views
from rest_framework.response import Response

from products.models import Product

from ..models import Comment
from .serializers import CommentSerializer


class ListCommentOfProductApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(product=self.request.query_params.get('product'), rating = 0, parent = None, deleted_by = None)

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.query_params.get('product'))
        serializer.save(product=product)
