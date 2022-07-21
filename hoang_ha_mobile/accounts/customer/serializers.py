from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .. import models
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "email",
            "birthday",
            "sex"
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

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ["id", "street", "ward", "district", "province"]

class ProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "birthday",
            "sex",
            'addresses'
        ]
