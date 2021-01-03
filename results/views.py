from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
from django.http import HttpResponse
from voter.models import Voter,Contestant
from .models import keys
import rsa
import base64
import time
from .forms import publicKeyUploadForm
import random
from django.contrib.auth.models import User
from .tasks import do_work
from .models import notaCount
from celery.result import AsyncResult

post_dictionary =[
    'VP',
    'HAB',
    'Tech',
    'Cult',
    'Welfare',
    'Sports',
    'SAIL',
    'SWC',
    'UGS',
    'PGS',
    'GS',      
]
users = []
try:
    users.append(User.objects.get(username='swc@iitg.ac.in'))
except:
    print("error in results/views.py")
try:    
    users.append(User.objects.get(username='alan@iitg.ac.in'))
except:
    print("error in results/views.py")
try:    
    users.append(User.objects.get(username='saketkumar@iitg.ac.in'))  
except:
    print("error 3")
 
def is_authorized(user):
    if user in users:
        return True
    return False

@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def keyUpload(request):
    publicKeys = keys.objects.filter(pubkey=True).values('user')
    public=[]
    for i in range(len(publicKeys)):
        public.append(User.objects.get(pk=publicKeys[i]['user']).first_name)
    privateKeys = keys.objects.filter(prikey=True).values('user')
    private=[]
    for i in range(len(privateKeys)):
        private.append(User.objects.get(pk=privateKeys[i]['user']).first_name)
    everyOne = []
    for i in range(len(users)):
        everyOne.append(users[i].first_name)
    return render(request,'keyinfo.html',{'public':public,'private':private,'Names':everyOne})
    

@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def publicKey(request):
    files = request.FILES.get('fileUpload', None)
    if request.method == 'POST' and files is not None:
        try:
            keys.objects.filter(user = request.user).delete()
        except:
            print("null")
        keys.objects.create(user=request.user,public_key=files,pubkey=True)
        return redirect('keyUpload')
    return render(request, 'pubKeyupload.html', {'keyType': 'Public'})


@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def privateKey(request):
    files = request.FILES.get('fileUpload', None)
    if request.method == 'POST' and files is not None:
        try:
            key=keys.objects.get(user=request.user)
        except:
            print("fucked up")
        key.private_key = files
        key.prikey = True
        key.save()
        return redirect('keyUpload')
    return render(request, 'pubKeyupload.html', {'keyType':'Private'})

running =None


@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def results(request):
    if request.method == 'POST':
        return redirect('results_view')
    global running
    if running is not None:
        res = AsyncResult(running)
        # if res.ready():
        # #   print('kya',res.result)
        #   task = do_work.delay()
        #   running = task.task_id
        
    else:
      task = do_work.delay()
      running = task.task_id
    try:
        key = keys.objects.get(user = request.user)
    except:
        key = None
    return render(request, 'results.html', {'task_id':running})   


@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def results_view(request):
    cont = []
    for post in post_dictionary:
        cont.append(post,Contestant.objects.filter(post=post))
    nota=notaCount.objects.all()
    return render(request,'results_view.html',{'Contestants':cont,'nota':nota})
