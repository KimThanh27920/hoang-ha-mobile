from asyncore import read
from email.policy import default
from xml.etree.ElementInclude import default_loader
from django.forms import ValidationError
from rest_framework import serializers
from comments.models import Comment
from accounts.administrator.serializers import UserSerializer
from products.models import Product
from products.administrator.serializers import ProductSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(source="created_by", read_only=True)
    updated_by = UserSerializer(read_only=True)
    deleted_by = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    type = serializers.SerializerMethodField(
        method_name="get_type", 
        read_only=True
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset = Comment.objects.all(),
        source = "parent",
        write_only = True,
        default = None
    )
    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "content",
            "author",
            "product",
            "product_id",
            "parent",
            "parent_id",
            "rating",
            "type",
            "created_at",
            "updated_by",
            "updated_at",
            "deleted_by",
            "deleted_at"
        ]
        read_only_fields = ["name","email","phone", "parent","rating"]

    def get_type(self, obj):
        if obj.rating != 0:
            return "review"
        return "comment"

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise ValidationError("Rating must be in range 0 to 5")
        return value
