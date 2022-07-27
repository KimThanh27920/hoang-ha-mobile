
from rest_framework import serializers

from ..models import Product
from categories.guest.serializers import ReadCategorySerializer
from variants.models import Variant


class VariantReadInProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'image',
            'color',
            'version',
            'price',
            'sale',
        ]

class ReadProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
        ]

        read_only_fields = [
            "id",
            "name",
            "description",
            "insurance",
            "category"
        ]

class ShortProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category"
        ]
class ReadDetailProductSerializer(serializers.ModelSerializer):
    product = ShortProductSerializer()

    # def get_product(self, obj):
    #     print(obj.category)
    #     return obj.id
    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "version",
            "price",
            "sale",
            "image"
        ]
