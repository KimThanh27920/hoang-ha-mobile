from rest_framework import serializers, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from articles.models import Article
from articles.models import Tag


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "deleted_by",
            "deleted_at",
        ]

class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "description",
            "author",
            "viewers",
            "status",
            "tags",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "deleted_by",
            "deleted_at",
        ]

    