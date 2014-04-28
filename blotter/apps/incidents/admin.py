from django.contrib.gis import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from apps.incidents.models import *

class IncidentAdmin(admin.ModelAdmin):
	list_display = ['code', 'agency', 'datetime_occurred']

class ArrestAdmin(admin.ModelAdmin):
	pass

class LocationAdmin(admin.OSMGeoAdmin):
	list_display=['name', 'address', 'point_location', 'point_verified', 'agency']
	default_lat = 4881940.078889836
	default_lon = -9821718.67269053
	default_zoom = 12
	
class CrimeAdmin(admin.ModelAdmin):
	list_display = ['name', 'code', 'nat_description', 'total_count', 'arrests']

admin.site.register(Crime, CrimeAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(Arrest, ArrestAdmin)
admin.site.register(Location, LocationAdmin)

