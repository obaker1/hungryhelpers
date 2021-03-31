from django.db import models


class Destinations(models.Model):
    text = models.TextField()


class GoogleMapsResponse(models.Model):
    location = models.TextField()
    distance = models.FloatField(default=0)
    time = models.TextField(default=0)
