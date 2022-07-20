from dataclasses import field
from rest_framework import serializers
from . import models
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = [
            "variant",
            "quantity",
        ]