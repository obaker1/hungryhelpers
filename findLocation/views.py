from django.contrib.sites import requests
from django.http import HttpResponse
from django.template import loader
import json
from urllib.parse import urlencode

API_KEY = '***REMOVED***'


def index(request):
    template = loader.get_template('findLocation/index.html')
    map_mode = 'place'
    endpoint = f"https://www.google.com/maps/embed/v1/{map_mode}"
    location = "Clarksburg, Maryland"
    src = f"{endpoint}?key={API_KEY}&q={location}"
    origin = 'Catonsville, Maryland'
    destinations = ['Towson, Maryland']
    return HttpResponse(template.render())#{'theUrl': src, 'origin': origin, 'destinations': destinations}))

# def distance():
#     base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
#     origins = ['Vancouver,BC', 'Seattle']
#     destination = ['San Francisco', 'Victoria, BC']
#
#     payload = {
#         'origins': '|'.join(origins),
#         'destinations': '|'.join(destination),
#         'mode': 'driving',
#         'api_key': API_KEY,
#         'units': 'imperial'
#     }
#
#     r = requests.GET(base_url, params=payload)
#     return json.loads(r)
