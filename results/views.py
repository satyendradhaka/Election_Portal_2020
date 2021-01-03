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
from celery.result import AsyncResult

# dicti={}
# positions=['vp','hab','tech','cult','sports','welfare','sail','swc','bsen','gsen']
# for i in positions:
#     dicti[i]={}
users = []
try:
    users.append(User.objects.get(username='swc@iitg.ac.in'))
    users.append(User.objects.get(username='alan@iitg.ac.in'))
    users.append(User.objects.get(username='saketkumar@iitg.ac.in'))  
except:
    print('error')
    
     
def is_authorized(user):
    if user in users:
        return True
    return False

 
@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def publicKey(request):
    publicKeys = keys.objects.filter(pubkey=True)
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            keys.objects.filter(user = request.user).delete()
        except:
            print("null")
        keys.objects.create(user=request.user,public_key=request.FILES['myfile'],pubkey=True)
    return render(request, 'pubKeyupload.html', {'pubKey':len(publicKeys)})


@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def privateKey(request):
    privateKeys = keys.objects.filter(prikey=True)
    if request.method == 'POST' and request.FILES['myfile']:
        # try:
        #     keys.objects.filter(user = request.user).delete()
        # except:
        #     print("null")
        key=keys.objects.get(user=request.user)
        key.private_key = request.FILES['myfile']
        key.prikey = True
        key.save()
    return render(request, 'pubKeyupload.html', {'pubKey':len(privateKeys)})

running =None


@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def results(request):
    done = True
    global running
    if running is not None:
        res = AsyncResult(running)
        if res.ready():
          # voters = Voter.objects.all().values_list('username',flat=True)
          task = do_work.delay()
          running = task.task_id
    else:
      task = do_work.delay()
      running = task.task_id
    try:
        key = keys.objects.get(user = request.user)
    except:
        key = None
    return render(request, 'results.html', {'key':key,'done':done,'task_id':running})   

