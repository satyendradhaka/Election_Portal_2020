from django.db import models
from django.contrib.auth.models import User
# Create your models here.copy
import os
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete

class keys(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    public_key = models.FileField(upload_to='public_key/',blank=True)
    private_key = models.FileField(upload_to='private_key/',blank=True)
    pubkey = models.BooleanField(default=False)
    prikey = models.BooleanField(default=False)
