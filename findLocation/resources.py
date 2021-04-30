from import_export import resources
from .models import GoogleMapsResponse
from .models import Origin

class GoogleMapsResponseResource(resources.ModelResource):
    class Meta:
        model = GoogleMapsResponse
        fields = ('location', 'distance', 'time', 'bus', 'school', 'address', 'timeframe', 'latitude', 'longitude')

class OriginResource(resources.ModelResource):
    class Meta:
        model = Origin
        fields = ('origin', 'latitude', 'longitude')