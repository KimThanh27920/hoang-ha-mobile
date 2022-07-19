from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "status",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "deleted_by",
            "deleted_at",
        ]
        # write_only_fields = [
        #     "deleted_by",
        #     "deleted_at",
        # ]
