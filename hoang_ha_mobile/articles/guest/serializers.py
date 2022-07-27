
from dataclasses import field
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from ..models import Article, Tag

from accounts.models import CustomUser

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "full_name"
        ]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name"
        ]

class ReadArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "author",
            "viewers",
            "tags",
            "image",
            "content",
            "created_at",
            "updated_at"
        ]

class ListArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "image",
            "description",
            "tags",
            "created_at",
            "updated_at"
        ]