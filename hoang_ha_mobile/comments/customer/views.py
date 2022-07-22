from urllib import request
from django.contrib.auth import get_user_model
User = get_user_model()
from . import serializers
from rest_framework import generics, permissions, filters, response, status
from .. import models
from rest_framework_simplejwt import authentication
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

class CommentListOwner(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['product']
    filterset_fields = ['product']
    def get_queryset(self):
        self.queryset = models.Comment.objects.filter(created_by = self.request.user.id)
        return super().get_queryset()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    
class RatingAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentRatingSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['product']
    filterset_fields = ['product']
    
    def get_queryset(self):    
        # return response.Response(data={"detail": "Rating existed, Can't create new instance"}, status=status.HTTP_404_NOT_FOUND)
        self.queryset = models.Comment.objects.filter( ~Q(rating=0),created_by = self.request.user.id)
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        
        rate = models.Comment.objects.filter(~Q(rating=0), created_by=self.request.user.id, product=self.request.data.get('product'))
        
        
        if(rate.exists()):    
            return response.Response(data={"detail": "Rating existed, Can't create new instance"}, status=status.HTTP_404_NOT_FOUND)
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # rate = models.Comment.objects.filter(~Q(rating=0), created_by=self.request.user.id, product=self.request.data.get('product'))
            
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    # serializer_class = serializers.CommentUpdateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_url_kwarg = 'comment_id'
            
    def get_serializer_class(self):
        if(self.request.method == "GET"):
            self.serializer_class = serializers.CommentRatingSerializer
        if(self.request.method == "PATCH" or self.request.method == "PUT"):
            self.serializer_class = serializers.CommentRatingUpdateSerializer                  
        return super().get_serializer_class()
    
    def get_queryset(self):
        if(self.request.method == "PUT" or self.request.method == "PATCH"):
            self.queryset = models.Comment.objects.filter( ~Q(rating=0), created_by = self.request.user.id)
        else:
            self.queryset = models.Comment.objects.filter(created_by = self.request.user.id)
        return super().get_queryset()
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    

        

