from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db.models.fields import CharField

class Voter(models.Model):
    username = models.CharField(max_length=100,unique=True) 
    # CATEGORY = (('0','UG-Boy'),
    #             ('1','UG-Girl'),
    #             ('2','PG-Boy'),
    #             ('3','PG-Girl'),)
    # HOSTELS = (
    #     ('0','HOSTEL NOT ALLOTED'),
    #     ('1','BRAHMAPUTRA'),
    #     ('2','DHANSIRI'),
    #     ('3','DIBANG'),
    #     ('4','DIHING'),
    #     ('5','DISANG'),
    #     ('6','KAMENG'),
    #     ('7','KAPILI'),
    #     ('8','LOHIT'),
    #     ('9','MANAS'),
    #     ('10','MARRIED SCHOLARS HOSTEL'),
    #     ('11','SIANG'),
    #     ('12','SUBHANSIRI'),
    #     ('13','UMIAM'),
    #     ('14','BARAK'),
    # )
    # category = models.CharField(max_length=1,choices=CATEGORY)
    final_submit = models.BooleanField(default=False) #0 if false 1 if true
    rollNumber = models.IntegerField(default=0, unique=True)
    dept = models.CharField(max_length=50, default='CSE')
    hostel = models.CharField(max_length=20,default='Lohit')
    vote_string1 = models.CharField(max_length=5000, default='')
    vote_string2 = models.CharField(max_length=5000, default='') 
    vote_time = models.CharField(max_length=100, default='')
    voter_location = PointField(default=Point(91.6916, 26.1878))
    voter_image = models.CharField(max_length=100, default='/images/voter/f.png')
    def __str__(self):
        return self.username


# contestants in the elections
class Contestant(models.Model):
    name = models.CharField(max_length=50,null=False)
    email = models.CharField(max_length=50,null=False)
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

    post = models.CharField(max_length=7, choices=CATEGORY)
    agenda1 = models.CharField(max_length=1000)
    agenda2 = models.CharField(max_length=1000)
    agenda3 = models.CharField(max_length=1000)
    agenda4 = models.CharField(max_length=1000)
    vote_count = models.IntegerField(default=0)
    rollNumber = models.IntegerField(default=0)
    pic = models.CharField(max_length=1000)
    random_suppling = models.IntegerField(default=0)
    tagline = models.CharField(max_length=1000, blank=True, default="Technology is my Middle Name!")
    agendaPDF = models.CharField(max_length=1000, blank=True, default="")
    # video = models.CharField(max_length=1000, blank=True, default="")

    def __str__(self):
        return self.name + " for " + self.post
