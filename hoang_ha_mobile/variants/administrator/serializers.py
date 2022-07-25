
from rest_framework import serializers

from variants.models import Variant
# from products.models import Product

#Serializer for POST, PUT, DELETE Variant
class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'color',
            'version',
            'image',
            'size',
            'strap',
            'general',
            'utilities',
            'network',
            'storage',
            'os_cpu',
            'front_cam',
            'camera',
            'pin',
            'screen',
            'price',
            'sale',
            'status',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
        ]


