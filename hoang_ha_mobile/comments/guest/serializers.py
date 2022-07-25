from dataclasses import field
from email.policy import default
from multiprocessing import parent_process
from rest_framework import serializers
from ..models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", 
            "image"
        ]

class ReplySerializer(serializers.ModelSerializer):
    created_by = CreateBySerializer()
    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "content",
            "created_at",
            "created_by",
            "parent"
        ]

        extra_kwargs = {
            'email': {'write_only': True},
            'phone': {'write_only': True},
            'parent': {'write_only': True}
        } 
class CommentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    replies = ReplySerializer(many=True, read_only=True)

    created_by = CreateBySerializer()
    # Reply multiple path
    # replies = serializers.SerializerMethodField()
    # def get_replies(self, obj):
    #     queryset = Comment.objects.filter(parent_id=obj.id)
    #     serializer = CommentSerializer(queryset, many=True)
    #     return serializer.data
    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "content",
            "created_at",
            "created_by",
            "replies",
        ]