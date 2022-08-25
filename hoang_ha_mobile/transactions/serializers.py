from rest_framework import serializers
from django.contrib.auth import get_user_model

from transactions.models import Transaction


User = get_user_model()

class UserReadInTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
        ]


#serializer for GET Product in Variant
class TransactionSerializerList(serializers.ModelSerializer):
    customer = UserReadInTransactionSerializer()
    class Meta:
        model = Transaction
        fields =[
            'id',
            'datetime' ,
            'type', 
            'amount',
            'currency',
            'description',
            'order',
            'customer',
            'payment_intent', 
            'last4',
        ]


