from django.contrib.gis import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from apps.incidents.models import *

class IncidentAdmin(admin.ModelAdmin):
	pass

class ArrestAdmin(admin.ModelAdmin):
	pass

class LocationAdmin(admin.OSMGeoAdmin):
	pass


admin.site.register(Incident, IncidentAdmin)
admin.site.register(Arrest, ArrestAdmin)
admin.site.register(Location, LocationAdmin)

