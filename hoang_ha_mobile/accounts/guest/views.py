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
from .serializers import AddressSerializer, MyTokenObtainPairSerializer, RegisterSerialize, PinSerializer, ChangePasswordWithPinSerializer
from ..models import Pin
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

        #Adding address
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

class ForgotPasswordApiView(APIView):

    def create_pin(self, user):
        pin = random.randint(100000, 999999)
        data = {
            'user': user.id,
            'pin': pin
        }
        # Tạo hoặc làm mới mã pin
        try:
            pin_user = Pin.objects.get(user = user.id)
            serializer = PinSerializer(instance=pin_user, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            serializer = PinSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save() 
        return pin

    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
        except:
            return Response({"message": "Nè email " + request.data['email'] + " này có đăng ký đâu mà lấy lại mật khẩu?"}, status=status.HTTP_404_NOT_FOUND)
        
        pin_code = self.create_pin(user)
        print(pin_code)

        html_content = render_to_string("index.html", {'fullname': user.full_name, 'pin': pin_code})
        send_mail(
            subject='Task Manager System - Forgot Password',
            message='Mật khẩu mới nè cha nội',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.data["email"]],
            html_message=html_content
        )
        return Response({"message": "Nè " + user.email + " có cái mật khẩu cũng không nhớ gửi qua email mật khẩu mới rồi đó."})

class ChangePasswordWithPINApiView(APIView):
    
    def disable_pin(self):
        self.pin.delete()

    def post(self, request):

        serializers = ChangePasswordWithPinSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            self.user = User.objects.get(email = request.data['email'])
            self.pin = Pin.objects.get(user = self.user.id)

            if int(request.data['pin']) == int(self.pin.pin):
                self.user.set_password(request.data['new_password'])
                self.user.save()
                self.disable_pin()
                return Response(data={"message" : "Change password is success"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message" : "Is valid PIN code"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data = {'message': "Account not found or No forgot password"}, status=status.HTTP_400_BAD_REQUEST)