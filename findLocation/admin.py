from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from findLocation.models import GoogleMapsResponse
from findLocation.models import Origin

@admin.register(GoogleMapsResponse)
# Register your models here.
class GoogleMapsResponseResource(ImportExportModelAdmin):
    fields = ('location', 'distance', 'time', 'bus','school', 'address','timeframe', 'latitude', 'longitude')
    pass

@admin.register(Origin)
class OriginResource(ImportExportModelAdmin):
    fields = ('origin', 'latitude', 'longitude')
    pass