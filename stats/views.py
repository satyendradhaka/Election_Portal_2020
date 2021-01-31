from typing import final
from django.shortcuts import render
from voter.models import Voter
from django.db.models import Q

# Create your views here.

def pollStats(request):

    #overall voted percentage
    total = Voter.objects.all().count()
    voted = Voter.objects.filter(final_submit = True).count()
    print(voted,'-',total)

    # UG PG voted students count
    totalUG = Voter.objects.filter(Q(category='0')|Q(category='1')).count() 
    totalPG = Voter.objects.filter(Q(category='2')|Q(category='3')).count() 
    ugVoted = Voter.objects.filter( ( Q(category='0') | Q(category='1') ) & Q(final_submit=True) ).count()
    pgVoted = Voter.objects.filter( ( Q(category='3') | Q(category='2') ) & Q(final_submit=True) ).count()
    print(totalUG,'-',totalPG,'-',ugVoted,'-',pgVoted)

    # Girls vote count
    totalGirls = Voter.objects.filter(Q(category='1') | Q(category='3')).count()
    girlsVoted = Voter.objects.filter( ( Q(category='1') | Q(category='3') ) & Q(final_submit=True) ).count()
    ugGirls = Voter.objects.filter(category='1').count()
    pgGirls = Voter.objects.filter(category='3').count()
    ugGirlsVoted = Voter.objects.filter( Q(category='1') & Q(final_submit=True)  ).count()
    pgGirlsVoted = Voter.objects.filter( Q(category='3') & Q(final_submit=True)  ).count()
    print(totalGirls, girlsVoted, ugGirlsVoted, pgGirlsVoted)
    return render(request,'stats.html',{'total': total, 'voted': voted, 'totalUG': totalUG, 'totalPG': totalPG, 'ugVoted': ugVoted, 'pgVoted': pgVoted, 'totalGirls': totalGirls, 'girlsVoted': girlsVoted, 'ugGirlsVoted': ugGirlsVoted, 'pgGirlsVoted': pgGirlsVoted, 'ugGirls': ugGirls, 'pgGirls': pgGirls})

def ugDeptStats(request):
    deptCount = {
        'CSE': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'MNC': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'Design': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'ME': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'CST': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'CL': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'EP': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'BT': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'CE': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'ECE': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'EEE': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'BSBE': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },
        'EEE': {
            'total': 0,
            'totalVoted': 0,
            'girls': 0,
            'girslVoted': 0
        },

    }

    for dept, count in deptCount.items():
        print(dept)
        if dept =='MNC':
            dept='MA'
        if dept == 'Design':
            dept = 'DD'
        count['total'] = Voter.objects.filter(( Q(category='0') | Q(category='1') ) & Q(dept=dept) ).count()
        count['totalVoted'] = Voter.objects.filter(( Q(category='0') | Q(category='1') ) & Q(dept=dept) & Q(final_submit=True) ).count()
        count['girls'] = Voter.objects.filter(Q(category='1') & Q(dept=dept) ).count()
        count['girlsVoted'] = Voter.objects.filter(Q(category='1') & Q(dept=dept) & Q(final_submit=True)).count()
        print(count)
    # print(deptCount)
    return render(request,'stats.html', deptCount)

