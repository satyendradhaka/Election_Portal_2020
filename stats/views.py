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

def deptFetchData():
    deptCount = {}
    jagrukDept = 0
    data = {}
    for i in deptList:
        total = Voter.objects.filter(dept = i).count()
        count = Voter.objects.filter(Q(dept=i) & Q(final_submit=True)).count()
        deptCount[i] = {'count':count,'total':total,'percent':(count*100)/total}
        if deptCount[i]['percent'] > jagrukDept:
            jagrukDept = deptCount[i]['percent']  
            data['jagrukDept']=i
    data['deptCount'] = deptCount
    return data

def totalVotersData():
    data = {}
    defaultCoords=25
    totalVoted = Voter.objects.filter(final_submit = True).count()
    data['totalVoted'] = [ i for i in f'{totalVoted:04}']
    totalVoters = Voter.objects.all().count()
    if totalVoted <=25:
        defaultCoords=totalVoted
    percent = (totalVoted*100)//totalVoters
    data['votePercent'] = [ i for i in f'{percent:02}']
    data['coords'] = random.sample([[coords[0].x,coords[0].y] for coords in Voter.objects.filter(final_submit=True).values_list('voter_location')], defaultCoords)
    return data    


def voteData(request):
    data = {}
    data.update(totalVotersData())
    data.update(deptFetchData())
    # print(data['coords'])
    return JsonResponse(data)


def stats(request):
    return render(request,'stats.html',{})


























































































































































































































































































































