from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse

from findLocation.models import Destinations
from findLocation.models import GoogleMapsResponse
import json
import requests


def index(request):
    destinations = Destinations.objects.filter()
    origin = '1000 Hilltop Cir, Baltimore, MD 21250, USA'
    callgooglematrix(origin)
    googlemaps = GoogleMapsResponse.objects.all().order_by('distance', 'location')
    context = {
        'destinations': destinations,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'origin': origin,
        'googlemapsresult': googlemaps,
    }
    return render(request, 'findLocation/index.html', context)


def callgooglematrix(origin):
    if Destinations.objects.count() > 0:
        destinationList = []
        for destinations in Destinations.objects.filter():
            destinationList.append(destinations.text)
        destinationAppended = '|'.join(destinationList)

        params = {
            'key': settings.GOOGLE_MAPS_API_KEY,
            'origins': origin,
            'destinations': destinationAppended
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
                newResponse = GoogleMapsResponse(location=location, distance=distance, time=time)
                newResponse.save()
        return result


def add(request):
    destination_text = request.POST['destination']
    if not Destinations.objects.filter(text=destination_text).exists():
        destination = Destinations(text=destination_text)
        destination.save()
    return HttpResponseRedirect(reverse('index'))
