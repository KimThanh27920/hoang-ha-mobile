from rest_framework import serializers
from django.contrib.auth import get_user_model

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