from django.shortcuts import render
from findLocation.models import GoogleMapsResponse


def staffPage(request):
    googlemaps = GoogleMapsResponse.objects.all()
    context={'googlemapsresult': googlemaps}
    return render(request, 'mealPlan/staffpage.html', context)