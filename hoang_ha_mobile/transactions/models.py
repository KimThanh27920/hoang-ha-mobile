from django.db import models
from django.contrib.auth import get_user_model

from orders.models import Order

# Create your models here.
User = get_user_model()

TYPES_CHOICES = [
    ("charge", "Charge"),
    ("refund", "Refund"),
]

class Transaction(models.Model):
    
    datetime = models.DateTimeField()
    type = models.CharField(default="charge",choices= TYPES_CHOICES,max_length=255)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    description = models.TextField(blank=True, null= True)
    last4 = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null= True)
    payment_intent = models.CharField(max_length=255)
    customer = models.ForeignKey(User, on_delete= models.PROTECT)
    
    class Meta:
        db_table = 'transactions'