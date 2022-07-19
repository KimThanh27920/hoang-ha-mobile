from urllib import request
from django.contrib.auth import get_user_model
User = get_user_model()
from .. import serializers
from rest_framework import generics, permissions, response, status
from .. import models
from django.shortcuts import get_object_or_404

class CommentListOwner(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(user = self.request.user.id)
        return super().get_queryset()