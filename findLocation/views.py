from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse

from findLocation.models import Destinations


def index(request):
    destinations = Destinations.objects.filter()
    context = {
        'destinations': destinations,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'origin': '1000 Hilltop Cir, Baltimore, MD 21250, USA'
    }
    return render(request, 'findLocation/index.html', context)


def add(request):
    destination_text = request.POST['destination']
    destination = Destinations(text=destination_text)
    destination.save()
    return HttpResponseRedirect(reverse('index'))
