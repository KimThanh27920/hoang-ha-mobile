from dataclasses import field
from pyexpat import model
import sre_compile
from rest_framework import serializers

from variants.models import Variant
from ..models import Order, OrderDetail

class ShortVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            ""
        ]

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

class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status'
        ]

class ListOrderSerializer(serializers.ModelSerializer):

    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        queryset = OrderDetail.objects.filter(order = obj.id)
        serializer = OrderDetailSerializer(queryset, many=True)
        return serializer.data[0]
    class Meta:
        model = Order
        fields = [
            'id',
            'shipping',
            'total',
            'status',
            'product'
        ]