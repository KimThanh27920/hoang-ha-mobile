
from rest_framework import serializers

from ..models import Category

class ReadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]

        read_only_fields = [
            "id",
            "name",
        ]