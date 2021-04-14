from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

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

# add custom origin from user
def addOrigin(request):
    global ORIGIN;
    origin_text = request.POST['origin'];
    if (origin_text != ''):
        ORIGIN = origin_text;

    for destination in GoogleMapsResponse.objects.all():
        params = {
            'key': settings.GOOGLE_MAPS_API_KEY,
            'origins': ORIGIN,
            'destinations': destination.location
        }
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?callback=initMap&libraries=&v=weekly&units=imperial'
        response = requests.get(url, params)
        try:
            result = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            result = "String could not be converted to JSON"

        # if response is empty
        if(result.get('status') != 'OK'):
            return HttpResponseRedirect(reverse('findlocation'))

        results = result['rows'][0]['elements'];
        destinationList = result['destination_addresses']

        location = destinationList[0]
        distanceString = results[0]['distance']['text']
        distanceString = distanceString.replace(',','');
        distance = float(distanceString[:-3])
        time = results[0]['duration']['text']
        GoogleMapsResponse.objects.filter(location=location).update(distance=distance, time=time)

    return HttpResponseRedirect(reverse('findlocation'))

# finds the distances for the destination and stores it in the database
def addLocation(request):
    destination_text = request.POST['destination']
    remove = request.POST['remove']
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

    # if response is empty
    if(result.get('status') != 'OK'):
        return HttpResponseRedirect(reverse('findlocation'))

    results = result['rows'][0]['elements'];
    destinationList = result['destination_addresses']

    for i in range(len(destinationList)):
        location = destinationList[i]
        distanceString = results[i]['distance']['text']
        distanceString = distanceString.replace(',','');
        distance = float(distanceString[:-3])
        time = results[i]['duration']['text']
        if not GoogleMapsResponse.objects.filter(location=location).exists():
            if (remove != 'r'):
                newResponse = GoogleMapsResponse(location=location, distance=distance, time=time, school=school, bus=bus)
                newResponse.save()
        else:
            if (remove == 'r'):
                GoogleMapsResponse.objects.filter(location=location).delete()
            else:
                GoogleMapsResponse.objects.filter(location=location).update(school=school, bus=bus)
    return HttpResponseRedirect(reverse('findlocation'))

