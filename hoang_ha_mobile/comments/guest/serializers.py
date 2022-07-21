from rest_framework import serializers
from ..models import Comment

class CommentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "content",
            "rating",
            "created_at",
            "product",
            "parent"
        ]