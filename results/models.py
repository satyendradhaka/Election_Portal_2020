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

class notaCount(models.Model):
    CATEGORY = (
        ('VP', 'General Secretary'),
        ('HAB', 'Mess Convener'),
        # ('UGS', 'Under Graduate Senator'),
        # ('PGS','Post Graduate Senator'),
        # ('GS','Girl Senator'),
        ('Tech','Technical Secretary'),
        ('Cult','Cultural Secretary'),
        ('Welfare','Welfare Secretary'),
        ('Sports','Sports Secretary'),
        ('SAIL','Maintenance Secretary'),
        ('SWC','Library Secretary'),
    )

    post = models.CharField(max_length=7, choices=CATEGORY,unique=True)
    vote_count = models.IntegerField(default=0)

class taskid(models.Model):
    task_id = models.CharField(max_length=100,unique=True)