
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

class ListImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            "id",
            'image',
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
    # product = ShortProductSerializer()

    # def get_product(self, obj):
    #     print(obj.category)
    #     return obj.id
    variants = VariantReadInProductSerializer(many=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        queryset = Variant.objects.filter(product = obj.id)
        serializer = ListImageProductSerializer(queryset, many=True)
        array = []
        for image in serializer.data:
            array.append(image['image'])
        return array
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "insurance",
            "variants",
            "description",
        ]
