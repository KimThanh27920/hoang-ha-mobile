from django.db import models
from django.apps import apps
from django.contrib.auth.models import  AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
# Create your models here.
#custom user model

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,unique=True)
    email = models.EmailField(_('email address'), unique=True)
    birthday = models.DateField(blank=True,null=True)
    sex = models.CharField(max_length=4)
    updated_at = models.DateTimeField(auto_now=True)
    block_at = models.DateTimeField(blank=True,null=True)
    updated_by = models.CharField(max_length=255)
    block_by = models.CharField(max_length=255,null=True)
   
    REQUIRED_FIELDS = ["email","phone"]


    def __str__(self):
        return self.full_name
