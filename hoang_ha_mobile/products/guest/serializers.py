
from rest_framework import serializers

from ..models import Product
from categories.guest.serializers import ReadCategorySerializer

class ReadProductSerializer(serializers.ModelSerializer):
    category = ReadCategorySerializer()
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "insurance",
            "status",
            "category"
        ]

        read_only_fields = [
            "id",
            "name",
            "description",
            "insurance",
            "status",
            "category"
        ]