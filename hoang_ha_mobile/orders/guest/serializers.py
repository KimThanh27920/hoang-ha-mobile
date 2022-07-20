from dataclasses import field
from rest_framework import serializers
from ..models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            'order',
            'variant',
            'price',
            'quantity',
        ]

        extra_kwargs = {
            "order": {"write_only": True}
        }


class OrderSerializer(serializers.ModelSerializer):

    order_details = OrderDetailSerializer(many=True, read_only=True)

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
            'total',
            'status',
            'order_details',
        ]
