from rest_framework import serializers
from .models import Product

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
        write_only_fields = [
            "deleted_by",
            "deleted_at",
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
        ]
# class ProductSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Product
#         fields =[
#             'id',
#             'name',
#             'description',
#             'insurance',
#             'category',
#             'created_at',
#             'created_by',
#             'updated_at',
#             'updated_by',
#             'deleted_at',
#             'deleted_by',
#         ]
