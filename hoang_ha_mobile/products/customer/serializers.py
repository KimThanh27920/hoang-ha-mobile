from rest_framework import serializers

from ..models import Product

from django.contrib.auth import get_user_model
User = get_user_model()

class ProductFavorite(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "favorite"
        ]
        
        