from django.db import models
from django.contrib.auth.models import User


class GoogleMapsResponse(models.Model):
    #id = models.CharField(max_length = 100, primary_key = True)
    location = models.TextField(default=0) # location textfield
    distance = models.FloatField(default=0)
    time = models.TextField(default=0)
    school = models.TextField(default=0)
    bus = models.TextField(default=0)
    timeframe = models.TextField(default=0) # distribution time for pickup
    address = models.TextField(default=0) # location address
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        db_table = "findLocation_googlemapsresponse"

class Origin(models.Model):
    user = models.ForeignKey(User, null=True, related_name="originID", on_delete=models.CASCADE)
    #id = models.CharField(max_length=100, primary_key=True)
    origin = models.TextField(default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        db_table = "findLocation_origin"