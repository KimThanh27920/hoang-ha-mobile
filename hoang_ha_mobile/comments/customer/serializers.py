from rest_framework import serializers
from .. import models
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "parent",
            "content",
            "product",
        ]
        
class CommentRatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "parent",
            "content",
            "product",
            "rating",
        ]
        
class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id"
            "content",
        ]
        

        
class RatingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "rating",
        ]