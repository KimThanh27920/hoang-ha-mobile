from dataclasses import field
from rest_framework import serializers
from ..models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            'variant',
            'price',
            'quantity',
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True)

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
            'order_detail'
        ]
