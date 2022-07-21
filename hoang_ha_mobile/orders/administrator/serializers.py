
from rest_framework import serializers
from orders.models import Order, OrderDetail
from variants.administrator.serializers import VariantReadSerializer

#serializer for POST,PUT, DELETE Order 
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
#serializer for POST,PUT, DELETE Order Detail 
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
#Serializer for GET Order Detail in Order 
# class OrderReadDetailSerializer(serializers.ModelSerializer):
#     variant = VariantReadSerializer(many=True,read_only=True)
#     class Meta:
#         model = OrderDetail
#         fields =[
#             'variant',
#             'price',
#             'quantity',
#             'created_at',
#             'created_by',
#             'updated_at',
#             'updated_by',
#             'deleted_at',
#             'deleted_by',
#         ]
class OrderReadDetailSerializer(serializers.ModelSerializer):
    variant = VariantReadSerializer()
    class Meta:
        model = OrderDetail
        fields =[
            'id',
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

#serializer for GET Order 
class OrderReadSerializer(serializers.ModelSerializer):
    order_details = OrderReadDetailSerializer(many=True, read_only=True)
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
            'order_details',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
            

        ]

#serializer for GET Order Detail 
class OrderDetailReadSerializer(serializers.ModelSerializer):
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