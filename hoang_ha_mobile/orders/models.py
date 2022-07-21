from django.db import models
from django.contrib.auth import get_user_model
from variants.models import Variant

User = get_user_model()

class Order(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=18, null=True)
    email = models.EmailField(null=True)
    shipping = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    note = models.TextField()
    status = models.CharField(default="Chờ xác nhận", max_length=255)
    total = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, related_name="user_create_order", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_update_order", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_order", null=True)

    class Meta:
        db_table = 'orders' 

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_details")
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,related_name="order_variant_details")
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_create_order_detail", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_update_order_detail", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_order_detail", null=True)


    class Meta:
        db_table = 'orders_detail' 