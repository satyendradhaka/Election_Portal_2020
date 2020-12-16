from django.shortcuts import render
from django.http import HttpResponse
from .models import UserGeoLocation
def save_user_geolocation(request):
    if request.method == 'POST':
        print("jkdslfbjskds")
        print(request.POST['latitude'])
        return render(request,'bla.html',{})
    return render(request,'bla.html',{})
    