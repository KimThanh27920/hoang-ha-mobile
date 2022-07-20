from rest_framework import serializers
from ..models import Variant
from products.guest.serializers import ReadProductSerializer

class ReadVarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            "id",
            "color",
            "storage",
            "price",
            "sale",
            "status",
            "product"
        ]


class ReadDetailVarianSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer()
    class Meta:
        model = Variant
        fields = [
            "id",
            "color",
            "version",
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
            "screen",
            "price",
            "sale",
            "status",
            "product"
        ]
