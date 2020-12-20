from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
# from pyuploadcare.dj.models import ImageField

class UserGeoLocation(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    coord = PointField()

# class Post(models.Model):
#     photo = ImageField(blank=True, manual_crop="")