# from typing import final
from django.db.models.expressions import Random
from django.shortcuts import render
from voter.models import Voter
from django.db.models import Q
from django.http import JsonResponse
import random
# Create your views here.
deptList =[
    'CSE',
    'ECE',
    'ME',
    'Civil',
    'Design',
    'BSBE',
    'CL',
    'EEE',
    'Physics',
    'Chemistry',
    'MNC',
    'HSS',
    'Energy',
    'Environment',
    'Nano-Tech',
    'Rural-Tech',
    'Linguistics',
]


def voteData(request):
    deptCount = {}
    jagruk = 0
    data = {}
    for i in deptList:
        total = Voter.objects.filter(dept = i).count()
        count = Voter.objects.filter(Q(dept=i) & Q(final_submit=True)).count()
        deptCount[i] = {'count':count,'total':total,'percent':(count*100)/total}
        if deptCount[i]['percent'] > jagruk:
            jagruk = deptCount[i]['percent']  
            data['jagruk']=i
    defaultCoords=25
    data['deptCount'] = deptCount
    data['totalVoted'] = Voter.objects.filter(final_submit = True).count()
    data['totalVoters'] = Voter.objects.all().count()
    if data['totalVoted'] <=25:
        defaultCoords=data['totalVoted']
    data['coords'] = random.sample([[coords[0].x,coords[0].y] for coords in Voter.objects.filter(final_submit=True).values_list('voter_location')], defaultCoords)
    print(data['coords'])
    return JsonResponse(data)


def stats(request):
    return render(request,'stats.html',{})









































































































































































































































































































































