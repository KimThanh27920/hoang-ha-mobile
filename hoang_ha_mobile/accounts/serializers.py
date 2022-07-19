from rest_framework import serializers
from django.contrib.auth import get_user_model
from dataclasses import field, fields
from importlib.metadata import requires
from pyexpat import model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "birthday",
            "sex",
            "updated_at",
            "block_at",
            "updated_by",
            "block_by"
        ]

class RegisterSerialize(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = [
            "username",
            "full_name",
            "phone",
            "email",
            "birthday",
            "sex",
            "password"

        ]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "birthday",
            "sex",
        ]
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['old_password', 'new_password']
        extra_kwargs = {
            'old_password': {'write_only':True},
            'new_password': {'write_only':True},
        }

