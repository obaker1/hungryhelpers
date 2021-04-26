from django.shortcuts import render
from findLocation.models import GoogleMapsResponse


def index(request):
    googlemaps = GoogleMapsResponse.objects.all()
    context={'googlemapsresult': googlemaps}
    return render(request, 'mealPlan/staffpage.html', context)