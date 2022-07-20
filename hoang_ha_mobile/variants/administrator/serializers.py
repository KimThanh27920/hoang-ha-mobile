import imp
from itertools import product
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser

from variants.models import Variant
from products.administrator.serializers import ProductSerializer

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'color',
            'version',
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

class VariantReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'color',
            'version',
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