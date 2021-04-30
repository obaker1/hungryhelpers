from django.db import models


class GoogleMapsResponse(models.Model):
    location = models.TextField(default=0) # location textfield
    distance = models.FloatField(default=0)
    time = models.TextField(default=0)
    school = models.TextField(default=0)
    bus = models.TextField(default=0)
    timeframe = models.TextField(default=0) # distribution time for pickup
    address = models.TextField(default=0) # location address
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

class Origin(models.Model):
    origin = models.TextField(default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)