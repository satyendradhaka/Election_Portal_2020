from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point

class Voter(models.Model):
    username = models.CharField(max_length=100) 
    CATEGORY = (('0','UG-Boy'),
                ('1','UG-Girl'),
                ('2','PG-Boy'),
                ('3','PG-Girl'),)
    category = models.CharField(max_length=1,choices=CATEGORY)
    final_submit = models.BooleanField(default=False) #0 if false 1 if true
    hostel = models.CharField(max_length=50, default='MANAS')
    dept = models.CharField(max_length=50, default='CSE')
    vote_string1 = models.CharField(max_length=5000, default='')
    vote_string2 = models.CharField(max_length=5000, default='') 
    vote_time = models.CharField(max_length=100, default='')
    voter_location = PointField(default=Point(0.0, 0.0))
    voter_image = models.CharField(max_length=100, default='/images/voter/f.png')
    def __str__(self):
        return self.username


# contestants in the elections
class Contestant(models.Model):
    name = models.CharField(max_length=50,null=False)
    email = models.CharField(max_length=50,null=False)
    CATEGORY = (
        ('VP', 'Vice President'),
        ('HAB', 'General Secretary of Hostel Affairs Board'),
        ('UGS', 'Under Graduate Senator'),
        ('PGS','Post Graduate Senator'),
        ('GS','Girl Senator'),
        ('Tech','General Secretary of Technical Board'),
        ('Cult','General Secretary of Cultural Board'),
        ('Welfare','General Secretary of Students\' Welfare Board'),
        ('Sports','General Secretary of Sports Board'),
        ('SAIL','General Seceratry of SAIL'),
        ('SWC','General Seceratry of SWC'),
    )

    post = models.CharField(max_length=7, choices=CATEGORY)
    agenda1 = models.CharField(max_length=1000)
    agenda2 = models.CharField(max_length=1000)
    agenda3 = models.CharField(max_length=1000)
    agenda4 = models.CharField(max_length=1000)
    vote_count = models.IntegerField(default=0)
    pic = models.CharField(max_length=1000)
    random_suppling = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name + " for " + self.post