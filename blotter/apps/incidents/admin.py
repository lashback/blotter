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


admin.site.register(Incident, IncidentAdmin)
admin.site.register(Arrest, ArrestAdmin)
admin.site.register(Location, LocationAdmin)

