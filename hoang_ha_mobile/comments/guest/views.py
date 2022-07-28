
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status


from variants.models import Variant

from ..models import Comment
from .serializers import CommentSerializer


class ListCommentOfProductApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(variant=self.request.query_params.get('variant'), rating=0, parent=None, deleted_by=None)

        
    def create(self, request, *args, **kwargs):
        request.data['email'] = request.data.get('email').lower()
        return super().create(request, *args, **kwargs)
