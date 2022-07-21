from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=18)
    content = models.TextField()
    rating = models.IntegerField(default = 0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", null=True)  
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_create_comment", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_update_comment", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_comment", null=True)

    class Meta:
        db_table = 'comments'
        