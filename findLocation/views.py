from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse

from findLocation.models import GoogleMapsResponse
import json
import requests

ORIGIN = '1000 Hilltop Cir, Baltimore, MD 21250, USA'


def findlocation(request):
    destinationList = []
    filter = []
    for destinations in GoogleMapsResponse.objects.filter():
        destinationList.append(destinations.location)
        filter.append(destinations.school)
        filter.append(destinations.bus)

    destinationAppended = '|'.join(destinationList) if destinationList else "None"
    filterAppended = '|'.join(filter) if filter else "None"
    googlemaps = GoogleMapsResponse.objects.all().order_by('distance', 'location')
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'origin': ORIGIN,
        'googlemapsresult': googlemaps,
        'destinationList': destinationAppended,
        'filter': filterAppended
    }
    return render(request, 'findLocation/index.html', context)


# finds the distances for the destination and stores it in the database
def addLocation(request):
    destination_text = request.POST['destination']
    school_text = request.POST['school']
    school = "F"
    if (school_text == "y"):
        school = "T"
    bus_text = request.POST['bus']
    bus = "F"
    if (bus_text == 'y'):
        bus = "T"
    params = {
        'key': settings.GOOGLE_MAPS_API_KEY,
        'origins': ORIGIN,
        'destinations': destination_text
    }
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?callback=initMap&libraries=&v=weekly&units=imperial'
    response = requests.get(url, params)
    try:
        result = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        result = "String could not be converted to JSON"

    results = result['rows'][0]['elements'];
    destinationList = result['destination_addresses']

    for i in range(len(destinationList)):
        location = destinationList[i]
        distanceString = results[i]['distance']['text']
        distance = float(distanceString[:-3])
        time = results[i]['duration']['text']
        if not GoogleMapsResponse.objects.filter(location=location, distance=distance).exists():
            newResponse = GoogleMapsResponse(location=location, distance=distance, time=time, school=school, bus=bus)
            newResponse.save()
        else:
            GoogleMapsResponse.objects.filter(location=location, distance=distance).update(school=school, bus=bus)
    return HttpResponseRedirect(reverse('findlocation'))
