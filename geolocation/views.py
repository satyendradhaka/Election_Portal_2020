from django.shortcuts import render
from django.http import HttpResponse
import json
from voter.models import Voter
from .models import Post
from .forms import PostForm

def save_user_geolocation(request):
    if request.method == 'POST':
        coord = json.loads(request.POST['data'])
        print(coord)
        latitude = coord['lat']
        longitude = coord['long']
        return render(request,'bla.html',{})
    return render(request,'bla.html',{})

def home(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = PostForm()

    try:
        posts = Post.objects.all()
    except Post.DoesNotExist:
        posts = None

    return render(request, 'image.html', { 'posts': posts, 'form': form })