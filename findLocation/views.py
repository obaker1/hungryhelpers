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
    locationList = []
    addressList = []
    filter = []
    for destinations in GoogleMapsResponse.objects.filter():
        locationList.append(destinations.location)
        addressList.append(destinations.address)
        filter.append(destinations.school)
        filter.append(destinations.bus)

    locationAppended = '|'.join(locationList) if locationList else "None"
    addressAppended = '|'.join(addressList) if addressList else "None"
    filterAppended = '|'.join(filter) if filter else "None"
    googlemaps = GoogleMapsResponse.objects.all().order_by('distance', 'address')
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'origin': ORIGIN,
        'googlemapsresult': googlemaps,
        'locationList': locationAppended,
        'addressList': addressAppended,
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
            'destinations': destination.address
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
        addressList = result['destination_addresses']

        address = addressList[0]
        distanceString = results[0]['distance']['text']
        distanceString = distanceString.replace(',','');
        distance = float(distanceString[:-3])
        time = results[0]['duration']['text']
        GoogleMapsResponse.objects.filter(address=address).update(distance=distance, time=time)

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
    addressList = result['destination_addresses']
    location = destination_text

    for i in range(len(addressList)):
        address = addressList[i]
        distanceString = results[i]['distance']['text']
        distanceString = distanceString.replace(',','');
        distance = float(distanceString[:-3])
        time = results[i]['duration']['text']
        if not GoogleMapsResponse.objects.filter(address=address).exists():
            if (remove != 'r'):
                newResponse = GoogleMapsResponse(location=location, distance=distance, time=time, school=school, bus=bus, address=address)
                newResponse.save()
        else:
            if (remove == 'r'):
                GoogleMapsResponse.objects.filter(address=address).delete()
            else:
                GoogleMapsResponse.objects.filter(address=address).update(location=location, school=school, bus=bus)
    return HttpResponseRedirect(reverse('findlocation'))