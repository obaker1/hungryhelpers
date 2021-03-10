from django.contrib.sites import requests
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
from urllib.parse import urlencode

API_KEY = '***REMOVED***'


def index(request):
    return render(request, 'findLocation/index.html', context={})