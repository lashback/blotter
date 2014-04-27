#from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response, get_object_or_404, render

from django.template import RequestContext
import datetime
from apps.incidents.models import *


def most_recent_incidents(request):
	incidents = Incident.objects.order_by('-datetime_reported')[:20]
	crimes = Crime.objects.order_by('-total_count')[:20]
	print incidents
	print crimes
	return render_to_response('incidents/recent.html', {'incidents': incidents, 'crimes':crimes})


def rough_hour(stamp):
	#implement hour-rounding. 
	hour = stamp.strftime('%I %p')
	return hour

def arrest_summary(request):
	arrests = Arrest.objects.order_by('-datetime')[:20]
	
	text = []
	for arrest in arrests:
		name = arrest.arrestee.name
		age = arrest.arrestee.age
		sex_abbreviated = arrest.arrestee.sex
		if sex_abbreviated == 'M':
			sex = "male"
		else:
			sex = "female"


		day = arrest.datetime.strftime('%A')
		hour = rough_hour(arrest.datetime)
		full_datetime = arrest.datetime.strftime("%b %d, %Y at %I:%M %p")
		charges = ''

		i = 0
		
		charges_query = arrest.charges.all()
		length = len(charges_query)
		if length == 1:
			charges = "the charge of " + charges_query[i].name.lower()
		else:
			charge = "charges of "
			while i < length:
				charge = charges_query[i].name.lower()
				if i == 0:
					charges += charge
				elif i == (length-1):
					charges += (" and " + charge)
				else:
					charges += (", " + charge)
				i += 1


		
		if arrest.location.name:
			location = arrest.location.name
		else:
			location = arrest.location.address
		
		incidents = arrest.incident_set.all()
		incident = incidents[0]
		location = location.title() + ", " + incident.agency.name.title()
		summary = incident.summary.lower()

		intro = "A %s-year-old %s was arrested %s around %s (%s) on %s at %s." % (age, sex, day, hour, full_datetime, charges, location)
		summary_section = "\nAccording to the report, %s" % summary
		alldis = intro+summary_section
		text.append(alldis)


	return render_to_response('incidents/arrests.html', {'arrests': text})

#def officer(self):
