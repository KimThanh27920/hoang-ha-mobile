from urllib import request
from django.contrib.auth import get_user_model
User = get_user_model()
from . import serializers
from rest_framework import generics, permissions, response, status
from .. import models
from rest_framework_simplejwt import authentication
from django.db.models import Q
from products.models import Product

class CommentListOwner(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(created_by = self.request.user.id)
        return super().get_queryset()
    
        
    
class CommentListProduct(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(created_by = self.request.user.id, product = self.kwargs['product_id']).select_related()
        return super().get_queryset()
    
    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs['product_id'])
        serializer.save(created_by=self.request.user, updated_by=self.request.user, product=product)
    
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_url_kwarg = 'comment_id'
    
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(created_by = self.request.user.id)
        return super().get_queryset()
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        

class RatingAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentRatingSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter( ~Q(rating=0),created_by = self.request.user.id, product=self.kwargs['product_id'])
        return super().get_queryset()
    
    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs['product_id'])
        serializer.save(created_by=self.request.user, updated_by=self.request.user, product=product)