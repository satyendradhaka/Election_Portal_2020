from django.shortcuts import render
from django.http import HttpResponse
import json
from voter.models import Voter

def save_user_geolocation(request):
    if request.method == 'POST':
        coord = json.loads(request.POST['data'])
        print(coord)
        latitude = coord['lat']
        longitude = coord['long']
        return render(request,'bla.html',{})
    return render(request,'bla.html',{})
    