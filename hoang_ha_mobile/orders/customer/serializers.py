from .. import models
from rest_framework import serializers
from variants.models import Variant

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
        ]
class OrderDetailReadOnlySerializer(serializers.ModelSerializer):
    variant = ReadVarianSerializer(read_only = True )
    class Meta:
        model = models.OrderDetail
        fields =[
            'order',
            'variant',
            'price',
            'quantity',
        ]
        extra_kwargs = {
            'order': {'write_only': True},
        }

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields =[
            'order',
            'variant',
            'price',
            'quantity',
        ]
        extra_kwargs = {
            'order': {'write_only': True},
        }
class OrderReadSerializer(serializers.ModelSerializer):
    order_details = OrderDetailReadOnlySerializer(many = True, read_only=True)
    class Meta:
        model = models.Order
        fields = [
            'id',            
            'shipping',            
            'total',
            'status',
            'order_details',
        ]

class OrderWriteSerializer(serializers.ModelSerializer):
    order_details = OrderDetailReadOnlySerializer(many = True, read_only=True)
    class Meta:
        model = models.Order
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'shipping',
            'delivery_address',
            'note',
            'total',
            'status',
            'order_details',
        ]