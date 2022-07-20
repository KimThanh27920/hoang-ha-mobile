from urllib import request
from django.contrib.auth import get_user_model
User = get_user_model()
from .. import serializers
from rest_framework import generics, permissions, response, status
from .. import models
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt import authentication

class CommentListOwner(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(phone = self.request.user.phone)
        return super().get_queryset()
    
class CommentListProduct(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(phone = self.request.user.phone, product = self.kwargs['product_id'])
        # self.queryset = listObject.objects.filter()
        return super().get_queryset()

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_url_kwarg = 'comment_id'
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(phone = self.request.user.phone)
        return super().get_queryset()