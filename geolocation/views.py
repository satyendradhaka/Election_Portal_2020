from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from voter.models import Voter
import base64
from .forms import FormWithCaptcha
from django.contrib.auth.decorators import login_required
# from .models import Post
# from .forms import PostForm

@login_required
def save_user_geolocation(request):
    if request.method == 'POST':
        coord = json.loads(request.POST['data'])
        request.session['latitude']=coord['lat']
        request.session['longitude']=coord['long']
        if request.session['latitude'] and request.session['longitude']:
            print('sfdf')
            request.session['location']= True
        print(coord)
    return redirect('captcha')

@login_required    
def save_user_image(request):
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
            request.session['image'] = True
        except Exception:
            print('i fucked up')
            return HttpResponse('something went wrong')
        return redirect('captcha')
    else:
        return redirect('captcha')

def home(request):
    return render(request, 'index.html', {})


@login_required
def verification(request):
    if not request.method=='POST':
        form = FormWithCaptcha()
        return render(request, 'verification.html', {'form': form})
        
    form = FormWithCaptcha(request.POST)
    if form.is_valid():
        print('u are not a robot')
        request.session['human']= True
        return redirect('vote')
    else:
        return redirect('captcha')
    return render(request, 'verification.html', {'form': form})
