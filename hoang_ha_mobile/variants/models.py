from django.db import models

from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

# Create your models here.



class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="variants")
    color = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    strap = models.CharField(max_length=255, null=True, blank=True)
    general = models.CharField(max_length=255, null=True, blank=True)
    utilities = models.CharField(max_length=255, null=True, blank=True)
    network = models.CharField(max_length=255, null=True, blank=True)
    storage = models.CharField(max_length=255, null=True, blank=True)
    os_cpu = models.CharField(max_length=255, null=True, blank=True)
    front_cam = models.CharField(max_length=255, null=True, blank=True)
    back_cam = models.CharField(max_length=255, null=True, blank=True)
    camera = models.CharField(max_length=255, null=True, blank=True)
    pin = models.CharField(max_length=255, null=True, blank=True)
    screen = models.CharField(max_length=255, null=True, blank=True)
    price = models.BigIntegerField(null=True)
    sale = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,related_name="user_create_variant", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,related_name="user_update_variant", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_variant", null=True)

    class Meta:
        db_table ='variant'