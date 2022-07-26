
from itertools import product
from rest_framework import generics, views
from rest_framework.response import Response

from variants.models import Variant

from ..models import Comment
from .serializers import CommentSerializer


class ListCommentOfProductApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(variant=self.request.query_params.get('variant'), rating = 0, parent = None, deleted_by = None)

    def perform_create(self, serializer):
        variant = Variant.objects.get(id=self.request.query_params.get('variant'))
        serializer.save(variant=variant)
