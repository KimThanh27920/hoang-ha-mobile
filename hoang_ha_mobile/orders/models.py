from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_create_category", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_update_category", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_category", null=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    insurance = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_create_product", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_update_product", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_product", null=True)

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="variants")
    color = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255, null=True)
    strap = models.CharField(max_length=255, null=True)
    general = models.CharField(max_length=255, null=True)
    utilities = models.CharField(max_length=255, null=True)
    network = models.CharField(max_length=255, null=True)
    storage = models.CharField(max_length=255, null=True)
    os_cpu = models.CharField(max_length=255, null=True)
    front_cam = models.CharField(max_length=255, null=True)
    back_cam = models.CharField(max_length=255, null=True)
    camera = models.CharField(max_length=255, null=True)
    pin = models.CharField(max_length=255, null=True)
    screen = models.CharField(max_length=255, null=True)
    price = models.BigIntegerField(null=True)
    sale = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_create_variant", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_update_variant", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_variant", null=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField(default=1)

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=18)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_create_comment", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_update_comment", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_comment", null=True)