from django.db import models


class GoogleMapsResponse(models.Model):
    location = models.TextField()
    distance = models.FloatField(default=0)
    time = models.TextField(default=0)
    school = models.TextField()
    bus = models.TextField()