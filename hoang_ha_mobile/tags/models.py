from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)      
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_create_tag", null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_update_tag", null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_delete_tag", null=True)