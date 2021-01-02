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
# from asgiref.sync import sync_to_async
# from background_task import background
# import  asyncio

# async def hello():
#   for i in range(6):
#     await  asyncio.sleep (10)
#     print(i)

dicti={}
positions=['vp','hab','tech','cult','sports','welfare','sail','swc','bsen','gsen']
for i in positions:
    dicti[i]={}

users = []
users.append(User.objects.get(username='swc@iitg.ac.in'))
users.append(User.objects.get(username='alan@iitg.ac.in'))
users.append(User.objects.get(username='saketkumar@iitg.ac.in'))
done_process = False

def vote_count(vote):
  k=vote.split(',')
  for i in range (10):
    if (i==9 or i==8):
      x=k[i].split(':')[1].strip()
      y=x[1:-1].split()
      for j in y:
        if (j in dicti[positions[i]]):
          dicti[positions[i]][j]=dicti[positions[i]][j]+1
        else: dicti[positions[i]][j]=1  
    else:  
      x=k[i].split(':')
      if (x[1] in dicti[positions[i]]):
        dicti[positions[i]][x[1]]=dicti[positions[i]][x[1]]+1
      else: 
        dicti[positions[i]][x[1]]=1

def decryptCipherText(cipher_text, vote_time):
  cipher_text = base64.b64decode(cipher_text.encode())
  cipher_text = xor(cipher_text, vote_time)
  file=[]
  file.append(keys.objects.get(user = users[0]))
  file.append(keys.objects.get(user = users[1]))
  file.append(keys.objects.get(user = users[2]))
#   file = keys.objects.get(user = request.user)
  for i in range(2, -1, -1):
    with open(file[i].private_key, "rb") as fr:
      pr = rsa.PrivateKey.load_pkcs1(fr.read())
    cipher_text = rsa.decrypt(cipher_text, pr)
  return cipher_text.decode()

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

running =None


@login_required
@user_passes_test(is_authorized,redirect_field_name="home")
def results(request):
    done = True
    global running
    if running is not None:
        res = AsyncResult(running)
        if res.ready():
          task = do_work.delay(20)
          running = task.task_id
    else:
      task = do_work.delay(20)
      running = task.task_id
    try:
        key = keys.objects.get(user = request.user)
    except:
        key = None
    return render(request, 'results.html', {'key':key,'done':done,'task_id':running})   

