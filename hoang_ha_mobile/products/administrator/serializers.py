from rest_framework import serializers
from products.models import Product
from variants.models import Variant


#Serializer for GET  Product Variant
class ProductReadInVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =[
            'id',
            'name',
            'description',
            'insurance',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
        ]
#Serializer for POST, PUT, DELETE Product
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields =[
            'id',
            'name',
            'description',
            'insurance',
            'category',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
        ]

#Serializer for GET Variant in Product
class VariantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
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
#Serializer for GET Product
class ProductReadSerializer(serializers.ModelSerializer):
    variants = VariantDetailSerializer(many= True, read_only = True)
    class Meta:
        model = Product
        fields =[
            'id',
            'name',
            'description',
            'insurance',
            'category',
            'variants',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
        ]
