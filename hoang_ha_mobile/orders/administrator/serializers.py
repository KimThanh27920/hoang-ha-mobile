
from rest_framework import serializers
from orders.models import Order, OrderDetail
from variants.administrator.serializers import VariantReadSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'shipping',
            'delivery_address',
            'note',
            'status',
            'total',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',

        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields =[
            'id',
            'order',
            'variant',
            'price',
            'quantity',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
        ]

class OrderReadDetailSerializer(serializers.ModelSerializer):
    variant = VariantReadSerializer()
    class Meta:
        model = OrderDetail
        fields =[
            'variant',
            'price',
            'quantity',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
        ]

class OrderReadSerializer(serializers.ModelSerializer):
    order_detail = OrderReadDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'shipping',
            'delivery_address',
            'note',
            'status',
            'total',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
            'order_detail'

        ]

class OrderDetailReadSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    variant = VariantReadSerializer()
    class Meta:
        model = OrderDetail
        fields =[
            'id',
            'order',
            'variant',
            'price',
            'quantity',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
        ]