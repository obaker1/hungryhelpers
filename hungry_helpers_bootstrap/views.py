from django.contrib.sites import requests
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from urllib.parse import urlencode

#API_KEY = '***REMOVED***'


def index(request):
    return render(request, 'hungry_helpers_bootstrap/index.html', context={})
    #return render(request, 'templates/dashboard/index.html', context={})