from django.contrib.sites import requests
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from urllib.parse import urlencode
from django.conf import settings

from findLocation.models import Destinations


def index(request):
    destinations = Destinations.objects.filter()
    context = {
        'destinations': destinations,
        'api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'findLocation/index.html', context)
