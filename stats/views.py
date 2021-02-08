# from typing import final
from django.shortcuts import render
from voter.models import Voter
from django.db.models import Q

# Create your views here.
deptList ={
    '01': 'CSE',
    '02': 'ECE',
    '03': 'ME',
    '04': 'Civil',
    '05': 'Design',
    '06': 'BSBE',
    '07': 'CL',
    '08': 'EEE',
    '21': ['Physics','EP'],
    '22': ['Chemistry','CST'],
    '23': 'MNC',
    '41': ['HSS','Development Studies'],
    '51': 'Energy',
    '52': 'Environment',
    '53': 'Nano-Tech',
    '54': 'Rural-Tech',
    '55': 'Linguistics'
}

def deptIdentify(rollNumber):
    roll = str(rollNumber)
    program= None
    if roll[2]=='0':
        program='UG'
    else:
        program="PG"
    dept=None
    
    if roll[4:6] != '21' and roll[4:6] != '22' and roll[4:6]!='41':
        dept = deptList(roll[4:6])
    elif roll[4:6]=='41':
        if roll[2:4]=='22':
            dept=deptList(roll[4:6])[1]
        else:
            dept=deptList(roll[4:6])[0]
    else:
        if program == 'UG':
            dept = deptList(roll[4:6])[1]
        else:
            dept = deptList(roll[4:6])[0]

    return program,dept