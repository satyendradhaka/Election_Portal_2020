import csv
import random
from django.utils.encoding import smart_str
from voter.models import Contestant, Voter

CHARS = "abcdefghjkmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789"

def csv_to_voter():
	csvfile = open('voter.csv', 'r')
	reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
	for i, row in enumerate(reader):
		print("voter", i+1)
		username = smart_str(row[0])
		category = smart_str(row[1])
		hostel = smart_str(row[2])
		dept = smart_str(row[3])
		vote_string=""
		vote_time = ""
		voter = Voter(username=username,
			category=category,
			hostel=hostel,
			dept=dept,
			vote_string = vote_string,
			vote_time= vote_time
		)

		voter.save()

def csv_to_contestants():
	csvfile = open('contestant.csv', 'r')
	reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
	for i, row in enumerate(reader):
		print("contestant ",i+1)
		contestant=Contestant(name=row[0],email = row[2], post = row[1], agenda1 = row[3], agenda2 = row[4], agenda3 = row[5], agenda4 = row[6], pic = "contestants/" + row[7] + ".jpg",  random_suppling = 0)
		contestant.save()

def run():
	Voter.objects.all().delete()
	Contestant.objects.all().delete()
	csv_to_voter()
	csv_to_contestants()	
