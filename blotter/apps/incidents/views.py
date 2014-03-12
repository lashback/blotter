#from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response, get_object_or_404, render

from django.template import RequestContext

from apps.incidents.models import *


def most_recent_incidents(request):
	incidents = Incident.objects.order_by('-datetime_reported')[:10]
	crimes = Crime.objects.order_by('-total_count')[:10]
	print incidents
	print crimes
	return render_to_response('incidents/recent.html', {'incidents': incidents, 'crimes':crimes})
