from django.core.management.base import BaseCommand, CommandError
import csv, os, sys, re
from time import strptime, strftime
from string import split
from apps.incidents.models import *
from django.contrib.gis.geos import GEOSGeometry
from settings.common import SITE_ROOT
from omgeo import Geocoder
from streetaddress import StreetAddressParser


class Command(BaseCommand):
	help = 'Uses OMGeocoder to geocode addresses and gives you results for the stragglers'
	
	def handle(self, *args, **options):
		parser = StreetAddressParser()
		try:
			g = Geocoder([
				['omgeo.services.Bing',{
					'settings':{
						'api_key':'AufKQbvq8uGM3qsQWwMwJNtlf6LLxe5bPvOAVcxi-79Qp0tDl0T2qScdOQiBNKkE'
					}
				}],
			])

			for s in Location.objects.filter(point_location__isnull=True):

				block_pattern = re.compile('BLOCK OF')
				cleaned_address = re.sub(block_pattern,'', s.address)
				if s.agency:
					address_string = cleaned_address + ", " + s.agency.name + " IL"
				else:
					address_string = cleaned_address + ", Champaign, IL"
				print address_string

					#homeless = address_string.find('HOMELESS')
					#print homeless
				
				if len(address_string) > 0:
					geocode_results = g.geocode(address_string,True)
					geocode_candidates = geocode_results['candidates']
					for c in geocode_candidates:
						if c.confidence == 'High':
							s.point_location = GEOSGeometry('POINT(%s %s)' % (c.x, c.y,),4326)
							s.save()
							self.stdout.write("Location found: %s %s\n" % (c.x, c.y,))
					
					if not s.point_location:
						self.stdout.write("No good geocode found for %s \n" % (address_string))
					s.attempted = True
					s.save()
		except (RuntimeError, TypeError, NameError):
			print "whoopsie"
			
