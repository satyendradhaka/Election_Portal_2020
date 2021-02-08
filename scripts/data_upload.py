import csv
import random
from django.utils.encoding import smart_str
from voter.models import Contestant, Voter
from django.contrib.gis.geos import Point

CHARS = "abcdefghjkmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789"

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
    '55': 'Linguistics',
	'61': 'Data Science',
	'62': 'FST-CL',
	'63': 'Emobility',

}

def deptIdentify(rollNumber):
    roll = rollNumber
    program= None
    if roll[2]=='0':
        program='UG'
    else:
        program="PG"
    dept=None
    
    if roll[4:6] != '21' and roll[4:6] != '22' and roll[4:6]!='41':
        dept = deptList[roll[4:6]]
    elif roll[4:6]=='41':
        if roll[2:4]=='22':
            dept=deptList[roll[4:6]][1]
        else:
            dept=deptList[roll[4:6]][0]
    else:
        if program == 'UG':
            dept = deptList[roll[4:6]][1]
        else:
            dept = deptList[roll[4:6]][0]

    return dept


def csv_to_voter():
	csvfile = open('voter.csv', 'r')
	reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
	for i, row in enumerate(reader):
		print("voter", i+1)
		username = smart_str(row[0]).lower()
		category = smart_str(row[1])
		rollNumber = smart_str(row[2])
		dept = deptIdentify(smart_str(row[2]))
		vote_string1=""
		vote_string2=""
		vote_time = ""
		voter_loc = Point(0.0,0.0)
		voter = Voter(username=username,
			category=category,
			rollNumber=int(rollNumber),
			dept=dept,
			vote_string1 = vote_string1,
			vote_string2 = vote_string2,
			vote_time= vote_time,
			voter_location = voter_loc
		)

		voter.save()

def csv_to_contestants():
	csvfile = open('contestant.csv', 'r')
	reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
	for i, row in enumerate(reader):
		print("contestant ",i+1)
		contestant=Contestant(name=row[0],email = row[2], post = row[1], agenda1 = row[3], agenda2 = row[4], agenda3 = row[5], agenda4 = row[6], pic = "contestants/" + row[7],  random_suppling = 0)
		contestant.save()

def run():
	Voter.objects.all().delete()
	Contestant.objects.all().delete()
	csv_to_voter()
	csv_to_contestants()	
