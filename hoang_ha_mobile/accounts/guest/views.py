import random
from shutil import ReadError
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt import tokens
from ..serializers import AddressSerializer, MyTokenObtainPairSerializer, RegisterSerialize
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

class LoginApiView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerialize
    queryset = User.objects.all()
    
    def perform_create(self, serializer):
        self.user = serializer.save()
          

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        new_user = User.objects.get(email=request.data['email'])
        # Init address for new user
        # address = {
        #     "user": new_user.id,
        #     "street": request.data['street'],
        #     "ward": request.data['ward'],
        #     "district": request.data['distric'],
        #     "province": request.data['province']
        # }
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=new_user)
        
        refresh = tokens.RefreshToken.for_user(self.user)
        refresh['email'] = request.data['email']
        data = {
            "user": response.data,
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
