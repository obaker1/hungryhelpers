from import_export import resources
from .models import GoogleMapsResponse
from .models import Origin

class GoogleMapsResponseResource(resources.ModelResource):
    class Meta:
        model = GoogleMapsResponse
        fields = ('id', 'location', 'distance', 'time', 'bus', 'school', 'address', 'timeframe', 'latitude', 'longitude')

class OriginResource(resources.ModelResource):
    class Meta:
        model = Origin
        fields = ('id', 'origin', 'latitude', 'longitude')