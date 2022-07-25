from rest_framework import serializers
from .. import models
        #  serializer child
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
        
class CommentRatingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "content",
            "rating"
        ]
        

        
# class RatingUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Comment
#         fields = [
#             "id",
#             "rating",
#         ]