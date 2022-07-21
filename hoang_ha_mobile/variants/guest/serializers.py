from itertools import product
from rest_framework import serializers
from ..models import Variant
from products.guest.serializers import ReadProductSerializer

class ShortInfoProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
class ReadVarianSerializer(serializers.ModelSerializer):
    product = ShortInfoProductSerializer()
    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "image",
            "color",
            "version",
            "price",
            "sale"
        ]


class ReadDetailVarianSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer()
    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "price",
            "sale",
            "color",
            "version",
            "image",
            "size",
            "strap",
            "general",
            "utilities",
            "network",
            "storage",
            "os_cpu",
            "front_cam",
            "camera",
            "pin",
            "screen"
        ]
