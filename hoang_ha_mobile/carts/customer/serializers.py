from rest_framework import serializers
from .. import models

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = [
            "id",
            "variant",
            "quantity",
        ]
        
class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = [
            "variant",
            "quantity",
        ]
        read_only_fields = ["variant"]