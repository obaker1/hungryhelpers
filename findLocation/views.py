from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse

from findLocation.models import GoogleMapsResponse
from findLocation.models import Origin

from findLocation.resources import GoogleMapsResponseResource
from findLocation.resources import OriginResource

import json
import requests

def findlocation(request):
    locationList = []
    addressList = []
    filter = []
    for destinations in GoogleMapsResponse.objects.all():
        locationList.append(destinations.location)
        addressList.append(destinations.address)
        filter.append(destinations.school)
        filter.append(destinations.bus)

    locationAppended = '|'.join(locationList) if locationList else "None"
    addressAppended = '|'.join(addressList) if addressList else "None"
    filterAppended = '|'.join(filter) if filter else "None"
    googlemaps = GoogleMapsResponse.objects.all().order_by('distance', 'address')
    origin = Origin.objects.first() # get origin from database
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'origin': origin.origin,
        'googlemapsresult': googlemaps,
        'locationList': locationAppended,
        'addressList': addressAppended,
        'filter': filterAppended
    }

    return render(request, 'findLocation/index.html', context)

# add custom origin from user
def addOrigin(request):
    origin_text = request.POST['origin'];
    Origin.objects.filter().update(origin=origin_text)

    for destination in GoogleMapsResponse.objects.all()[:10]:
        params = {
            'key': settings.GOOGLE_MAPS_API_KEY,
            'origins': origin_text,
            'destinations': destination.address
        }
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?callback=initMap&libraries=&v=weekly&units=imperial'
        response = requests.get(url, params)
        try:
            result = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            result = "String could not be converted to JSON"

        # if response is empty
        if(result.get('status') != 'OK' or result['rows'][0]['elements'][0].get('status') != 'OK'):
            return HttpResponseRedirect(reverse('findlocation'))

        results = result['rows'][0]['elements'];
        addressList = result['destination_addresses']

        location = destination.location
        distanceString = results[0]['distance']['text']
        distanceString = distanceString.replace(',','')
        distance = float(distanceString[:-3])
        time = results[0]['duration']['text']
        GoogleMapsResponse.objects.filter(location=location).update(distance=distance, time=time)

    return HttpResponseRedirect(reverse('findlocation'))

# finds the distances for the destination and stores it in the database
def addLocation(request):
    destination_text = request.POST['destination']
    remove = request.POST['remove']
    timeframe = request.POST['timeframe']
    if (timeframe == ""):
        timeframe = "N/A"
    school_text = request.POST['school']
    school = "F"
    if (school_text == "y"):
        school = "T"
    bus_text = request.POST['bus']
    bus = "F"
    if (bus_text == 'y'):
        bus = "T"
    origin = Origin.objects.first() # get origin from database
    params = {
        'key': settings.GOOGLE_MAPS_API_KEY,
        'origins': origin.origin,
        'destinations': destination_text
    }
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?callback=initMap&libraries=&v=weekly&units=imperial'
    response = requests.get(url, params)
    try:
        result = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        result = "String could not be converted to JSON"
    # if response is empty
    if(result.get('status') != 'OK' or result['rows'][0]['elements'][0].get('status') != 'OK'):
        return HttpResponseRedirect(reverse('findlocation'))
    results = result['rows'][0]['elements'];
    addressList = result['destination_addresses']
    location = destination_text

    # get latitude and longitude of location
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'key': settings.GOOGLE_MAPS_API_KEY,
        'address': destination_text,
        'sensor': 'false',
    }
    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    # Use the first result
    result = res['results'][0]
    lat = result['geometry']['location']['lat']
    lng = result['geometry']['location']['lng']

    # runs once to add/update/remove a location
    for i in range(len(addressList)):
        address = addressList[i]
        distanceString = results[i]['distance']['text']
        distanceString = distanceString.replace(',','');
        distance = float(distanceString[:-3])
        time = results[i]['duration']['text']
        if not GoogleMapsResponse.objects.filter(address=address).exists():
            if (remove != 'r'):
                newResponse = GoogleMapsResponse(location=location, distance=distance, time=time, school=school, bus=bus, address=address, timeframe=timeframe, latitude=lat, longitude=lng)
                newResponse.save()
        else:
            if (remove == 'r'):
                GoogleMapsResponse.objects.filter(address=address).delete()
            else:
                GoogleMapsResponse.objects.filter(address=address).update(location=location, school=school, bus=bus, timeframe=timeframe, latitude=lat, longitude=lng)
    return HttpResponseRedirect(reverse('findlocation'))

def export(request):
    response_resource = GoogleMapsResponseResource()
    dataset = response_resource.export()
    response = HttpResponse(dataset.xls, content_type = 'text/excel')
    response['Content-Disposition'] = 'attachment; filename = GoogleMapsResponse.xls'
    return response