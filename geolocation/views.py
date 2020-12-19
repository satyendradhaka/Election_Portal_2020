from django.shortcuts import render
from django.http import HttpResponse
import json
from voter.models import Voter
import base64
# from .models import Post
# from .forms import PostForm

def save_user_geolocation(request):
    if request.method == 'POST':
        coord = json.loads(request.POST['data'])
        print(coord)
        latitude = coord['lat']
        longitude = coord['long']
        return render(request,'bla.html',{})
    return render(request,'bla.html',{})


def home(request):
    username = request.user.username
    image_name = request.user.last_name + ".png"
    if Voter.objects.all().filter(username=username).exists():
        voter = Voter.objects.get(username=username)
    else:
        return HttpResponse('get the fuck out of here')
    if request.method == 'POST':
        imagebase64= request.POST['imagebase64data']
        try:
            with open("images/voters/"+image_name, "wb") as fh:
                fh.write(base64.b64decode(imagebase64))
            voter.voter_image= "images/voters/"+image_name
            voter.save()
        except Exception:
            return HttpResponse('something went wrong')
        return render(request, 'image.html', {})
    else:
        return render(request, 'image.html', {})