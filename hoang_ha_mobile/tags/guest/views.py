from ast import Delete
from rest_framework import generics
from tags.models import Tag
from .serializers import TagSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, filters
from datetime import datetime

class ListTagApiView(generics.ListAPIView):
    queryset = Tag.objects.filter(deleted_by = None)
    serializer_class = TagSerializer
    pagination_class = None