from .. import models
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
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
            'status',
            'total',
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields =[
            'id',
            'order',
            'variant',
            'price',
            'quantity',
        ]