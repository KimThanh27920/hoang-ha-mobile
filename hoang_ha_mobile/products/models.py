from email.policy import default
from django.db import models
from categories.models import Category

from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    insurance = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,related_name="user_create_product", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,related_name="user_update_product", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_product", null=True)

    class Meta:
        db_table = 'products' 

    def __str__(self):
        return self.name