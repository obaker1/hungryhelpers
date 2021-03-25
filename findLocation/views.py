from django.contrib.sites import requests
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from urllib.parse import urlencode

API_KEY = '***REMOVED***'

from findLocation.models import Destinations

def index(request):
    destinations = Destinations.objects.filter()
    context = {
        'destinations' : destinations
    }
    return render(request, 'findLocation/index.html', context={})