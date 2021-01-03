from celery import shared_task
import time
from celery_progress.backend import ProgressRecorder
from voter.models import Voter,Contestant
from django.contrib.auth.models import User
from .decrypt import decryptCipherText

dicti={}
positions=['vp','hab','tech','cult','sports','welfare','sail','swc','bsen','gsen']
for i in positions:
  dicti[i]={}

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

@shared_task(bind=True)
def do_work(self):
    progress_recorder = ProgressRecorder(self)
    voters = Voter.objects.all().filter(final_submit=True)
    for i in range(len(voters)):
        print(voters[i])
        vote_string = decryptCipherText(voters[i].vote_string1,voters[i].vote_time)+decryptCipherText(voters[i].vote_string2,voters[i].vote_time)
        print(vote_string)
        vote_count(vote_string)
        progress_recorder.set_progress(i+1,len(voters))
    print(dicti)
    return 'work is complete'