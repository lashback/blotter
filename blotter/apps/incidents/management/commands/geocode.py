from django.core.management.base import BaseCommand, CommandError
import csv, os, sys, re
from time import strptime, strftime
from string import split
from apps.incidents.models import *
from django.contrib.gis.geos import GEOSGeometry
from settings.common import SITE_ROOT
from omgeo import Geocoder
from streetaddress import StreetAddressParser
import math

class Command(BaseCommand):
	help = 'Uses OMGeocoder to geocode addresses and gives you results for the stragglers'
	
	def handle(self, *args, **options):
			parser = StreetAddressParser()
		#try:
			g = Geocoder([
				['omgeo.services.Bing',{
					'settings':{
						'api_key':'AufKQbvq8uGM3qsQWwMwJNtlf6LLxe5bPvOAVcxi-79Qp0tDl0T2qScdOQiBNKkE'
					}
				}],
			])

			for location in Location.objects.filter(point_location__isnull=True):
				string = location.address.strip()

				if location.city is not None:
					string = string + ", " + location.city
				
				else:
					if location.agency:
						string = string + ", " + location.agency.name + " IL"
					else:
						string = string + ", Champaign, IL"
				
				block_pattern = re.compile('BLOCK OF')
				cleaned_address = re.sub(block_pattern,'', string)
				print cleaned_address
				
				if location.intersection_indicator:
					slash = re.compile('/')
					string = re.sub(slash,'at', string)
					print string

				if len(location.address.strip()) > 0:
					geocode_results = g.geocode(cleaned_address,True)
					geocode_candidates = geocode_results['candidates']
					for c in geocode_candidates:

						if math.floor(c.x) == -89.0 and math.floor(c.y) == 40.0:
							print "within acceptable ranges"
							if c.confidence == 'High':
								location.point_location = GEOSGeometry('POINT(%s %s)' % (c.x, c.y,),4326)
								location.save()
								self.stdout.write("Location found: %s %s\n" % (c.x, c.y,))
					
					if not location.point_location:
						self.stdout.write("No good geocode found for %s \n" % (cleaned_address))
					#location.attempted = True				
					location.save()

		#except (RuntimeError, TypeError, NameError):
		#	print "whoopsie"