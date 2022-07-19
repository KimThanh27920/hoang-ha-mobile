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
from ..serializers import MyTokenObtainPairSerializer

# Create your views here.

class LoginApiView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

