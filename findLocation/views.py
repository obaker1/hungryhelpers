from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse
from datetime import time

from findLocation.models import GoogleMapsResponse, Origin
from mealPlan.models import Meal

from findLocation.resources import GoogleMapsResponseResource

import json
import requests
import math


def findlocation(request):
    result = [''] * 5
    if (Origin.objects.all() and GoogleMapsResponse.objects.all()):
        if (GoogleMapsResponse.objects.all().count() < 10):
            result = getLocations(GoogleMapsResponse.objects.all().count())
        else:
            result = getLocations(10)
    elif (Origin.objects.all()):  # if only the origin exists in database
        result[0] = Origin.objects.first().origin
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'origin': result[0],
        'googlemapsresult': result[1],  # shortenedList
        'locationList': result[2],  # locationAppended
        'addressList': result[3],  # addressAppended
        'filter': result[4],  # filterAppended
    }
    return render(request, 'findLocation/index.html', context)


# add custom origin from user
def addOrigin(request):
    origin_text = request.POST['origin'];
    # get latitude and longitude of origin
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'key': settings.GOOGLE_MAPS_API_KEY,
        'address': origin_text,
        'sensor': 'false',
    }
    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    # Use the first result
    result = res['results'][0]
    lat = result['geometry']['location']['lat']
    lng = result['geometry']['location']['lng']
    if (not Origin.objects.all()):  # create new origin if not existing
        newOrigin = Origin(origin=origin_text, latitude=lat, longitude=lng)
        newOrigin.save()
    else:
        Origin.objects.filter().update(origin=origin_text, latitude=lat, longitude=lng)
    origin = Origin.objects.first()  # get origin from database

    distList = []
    # find 10 closest places from origin
    for destinations in GoogleMapsResponse.objects.all():
        dist = math.sqrt(
            ((origin.latitude - destinations.latitude) ** 2) + ((origin.longitude - destinations.longitude) ** 2))
        distList.append(dist)
    distList.sort()
    distList = distList[:10]
    # update distance of the 10 closest places into the database
    for destinations in GoogleMapsResponse.objects.all():
        dist = math.sqrt(
            ((origin.latitude - destinations.latitude) ** 2) + ((origin.longitude - destinations.longitude) ** 2))
        if (dist in distList):
            params = {
                'key': settings.GOOGLE_MAPS_API_KEY,
                'origins': origin_text,
                'destinations': destinations.address
            }
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?callback=initMap&libraries=&v=weekly&units=imperial'
            response = requests.get(url, params)
            try:
                result = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                result = "String could not be converted to JSON"

            # if response is empty
            if (result.get('status') != 'OK' or result['rows'][0]['elements'][0].get('status') != 'OK'):
                return HttpResponseRedirect(reverse('findlocation'))

            results = result['rows'][0]['elements'];
            addressList = result['destination_addresses']

            location = destinations.location
            distanceString = results[0]['distance']['text']
            distanceString = distanceString.replace(',', '')
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
    temp = False
    if (not Origin.objects.first()):  # create temporary origin if no origin exists
        temp = True
        newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213,
                           longitude=-76.7143524)
        newOrigin.save()
    origin = Origin.objects.first()  # get origin from database
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
    if (result.get('status') != 'OK' or result['rows'][0]['elements'][0].get('status') != 'OK'):
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

    # add new destination to database
    address = addressList[0]
    if (temp):
        distance = 0
        time = 'N/A'
    else:
        distanceString = results[0]['distance']['text']
        distanceString = distanceString.replace(',', '');
        distance = float(distanceString[:-3])
        time = results[0]['duration']['text']
    if not GoogleMapsResponse.objects.filter(address=address).exists():
        if (remove != 'r'):
            newResponse = GoogleMapsResponse(location=location, distance=distance, time=time, school=school, bus=bus,
                                             address=address, timeframe=timeframe, latitude=lat, longitude=lng)
            newResponse.save()
    else:
        if (remove == 'r'):
            GoogleMapsResponse.objects.filter(address=address).delete()
        else:
            GoogleMapsResponse.objects.filter(address=address).update(location=location, school=school, bus=bus,
                                                                      timeframe=timeframe, latitude=lat, longitude=lng)
    if (temp):  # remove temporary origin
        Origin.objects.all().delete()
    return HttpResponseRedirect(reverse('findlocation'))


def addMore(request):
    result = [''] * 5
    if (Origin.objects.all() and GoogleMapsResponse.objects.all()):
        if (GoogleMapsResponse.objects.all().count() < 20):
            result = getLocations(GoogleMapsResponse.objects.all().count(), True)
        else:
            result = getLocations(20, True)
    elif (Origin.objects.all()):  # if only the origin exists in database
        result[0] = Origin.objects.first().origin
    context = {
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'origin': result[0],
        'googlemapsresult': result[1],  # shortenedList
        'locationList': result[2],  # locationAppended
        'addressList': result[3],  # addressAppended
        'filter': result[4],  # filterAppended,
    }
    return render(request, 'findLocation/index.html', context)


def getLocations(num, more=False, originObj=None, destinationsObj=None):
    temp = 10
    if (num > 10 and more):  # if asking for more locations
        temp = num
        num = 10
    locationList = [''] * num
    addressList = [''] * num
    filter = [''] * num * 2
    distList = []  # contains the distances between origin and destinations by latitude and longitude
    sortDist = []  # contains the calculated time between origin and destinations
    shortenedList = [''] * num

    if originObj != None:
        origin = originObj
    else:
        origin = Origin.objects.first()  # get origin from database
    if destinationsObj == None:
        destinationsObj = GoogleMapsResponse.objects.all()

    # find 10 closest places from origin
    for destinations in destinationsObj:
        dist = math.sqrt(
            ((origin.latitude - destinations.latitude) ** 2) + ((origin.longitude - destinations.longitude) ** 2))
        distList.append(dist)
        sortDist.append(destinations.time)
    distList, sortDist = (list(t) for t in zip(*sorted(
        zip(distList, sortDist))))  # sort distList by distance and sort sortDist the same way
    if (temp >= 10):
        distList = distList[temp - 10:temp]
        sortDist = sortDist[temp - 10:temp]
    sortDist, distList = (list(t) for t in
                          zip(*sorted(zip(sortDist, distList))))  # sort sortDist by time and sort distList the same way
    # set 10 closest places to variables that will be added onto the map
    for destinations in destinationsObj:
        dist = math.sqrt(
            ((origin.latitude - destinations.latitude) ** 2) + ((origin.longitude - destinations.longitude) ** 2))
        if (dist in distList):
            idx = distList.index(dist)
            locationList[idx] = destinations.location
            addressList[idx] = destinations.address
            filter[idx * 2] = destinations.school
            filter[idx * 2 + 1] = destinations.bus
            shortenedList[idx] = destinations.location + ': ' + str(
                destinations.distance) + ' miles in ' + destinations.time + ' (' + destinations.timeframe + ')'

    locationAppended = '|'.join(locationList) if locationList else "None"
    addressAppended = '|'.join(addressList) if addressList else "None"
    filterAppended = '|'.join(filter) if filter else "None"

    return origin.origin, shortenedList, locationAppended, addressAppended, filterAppended


def export(request):
    response_resource = GoogleMapsResponseResource()
    dataset = response_resource.export()
    response = HttpResponse(dataset.xls, content_type='text/excel')
    response['Content-Disposition'] = 'attachment; filename = GoogleMapsResponse.xls'
    return response


def filteringLocations(mealplanform, theStudent):
    deletearr = []


    pickup_type = mealplanform.pickup_type
    pickup_time = mealplanform.time.split('-')
    start_time = convertmilitarytime(pickup_time[0].split(':'))
    end_time = convertmilitarytime(pickup_time[1].split(':'))

    # filter locations by pickup type
    if pickup_type == "School":
        newDestinations = GoogleMapsResponse.objects.filter(school='T')
    else:
        newDestinations = GoogleMapsResponse.objects.filter(bus='T')

    for destinations in newDestinations:
        deletebool = False

        # filter locations by meals
        goodmeals = Meal.objects.filter(location=destinations)
        deletemeals = []
        for filteredmeals in goodmeals:
            mealdelete = False
            if theStudent.allergic_celiac == "Yes" and filteredmeals.celiac == False:
                mealdelete = True
            if theStudent.allergic_shellfish == "Yes" and filteredmeals.shellfish == False:
                mealdelete = True
            if theStudent.allergic_lactose == "Yes" and filteredmeals.lactose == False:
                mealdelete = True
            if theStudent.preference_halal == "Yes" and filteredmeals.halal == False:
                mealdelete = True
            if theStudent.preference_kosher == "Yes" and filteredmeals.kosher == False:
                mealdelete = True
            if theStudent.preference_vegetarian == "Yes" and filteredmeals.vegetarian == False:
                mealdelete = True
            if mealdelete == True:
                deletemeals.append(filteredmeals.pk)

        for deleting in deletemeals:
            goodmeals=goodmeals.exclude(pk=deleting)

        if goodmeals.count() == 0:
            deletebool=True

        # if location is not deleted my meals, filter locations by pickup date/time
        if deletebool==False:
            datetimeframe = destinations.timeframe.split(' ')
            if len(datetimeframe) == 1:
                schooltime = datetimeframe[0].split('-')
            else:
                day = datetimeframe[0]
                if day != mealplanform.day:
                    deletebool = True
                schooltime = datetimeframe[1].split('-')

            schooltime[0] = schooltime[0].split(':')
            schooltime[1] = schooltime[1].split(':')

            schooltime[0] = convertmilitarytime(schooltime[0])
            schooltime[1] = convertmilitarytime(schooltime[1])
            if time(start_time[0], start_time[1]) < time(schooltime[0][0], schooltime[0][1]) and time(end_time[0], end_time[1]) > time(schooltime[1][0], schooltime[1][1]):
                deletebool = True
        if deletebool == True:
            deletearr.append(destinations.pk)

    print(len(deletearr))

    for deleting in deletearr:
        newDestinations = newDestinations.exclude(pk=deleting)

    for destinations in newDestinations:
        print(destinations.location)
    return newDestinations


def convertmilitarytime(theTime):
    if len(theTime) == 1:
        hrs = str(theTime[0][:-2])
        min = '00'
        part = str(theTime[0][-2:])
        theTime[0] = hrs
        theTime.append(min + part)
    if theTime[0] == '12':
        theTime[0] = '00'
    if theTime[1][2] == 'p':
        newtime = int(theTime[0])
        theTime[0] = str(newtime + 12)
    theTime[0] = int(theTime[0])
    theTime[1] = int(theTime[1][0:2])
    return theTime
