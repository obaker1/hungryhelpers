from django.db import models


class GoogleMapsResponse(models.Model):
    location = models.TextField() # location textfield
    distance = models.FloatField(default=0)
    time = models.TextField(default=0)
    school = models.TextField()
    bus = models.TextField()
    timeframe = models.TextField(default="M/W 11am-1pm") # distribution time for pickup
    address = models.TextField() # location address