from typing import final
from django.shortcuts import render
from voter.models import Voter
from django.db.models import Q

# Create your views here.

def pollPercent(request):
    total = Voter.objects.all().count()
    voted = Voter.objects.filter(final_submit = True).count()
    print(voted,'-',total)
    return render(request,'stats.html',{})

def UgPgStats(request):
    totalUG = Voter.objects.filter(Q(category='0')|Q(category='1')).count() 
    totalPG = Voter.objects.filter(Q(category='2')|Q(category='3')).count() 
    ugVoted = Voter.objects.filter( ( Q(category='0') | Q(category='1') ) & Q(final_submit=True) ).count()
    pgVoted = Voter.objects.filter( ( Q(category='3') | Q(category='2') ) & Q(final_submit=True) ).count()
    print(totalUG,'-',totalPG,'-',ugVoted,'-',pgVoted)
    return render(request,'stats.html',{})