from django.db import models
from django.contrib.auth.models import User

# Create your models here.

'''
class Choices(models.Model):
    RESTRICTIONS =(
        ("1", "Celiac"),
        ("2", "Shellfish"),
        ("3", "Lactose"),
        ("4", "Halal"),
        ("5", "Kosher"),
        ("6", "Vegetarian")
    )
'''

class Meal(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    #restrictions = models.ManyToManyField(Choices)

    celiac = models.BooleanField(default=False)
    shellfish = models.BooleanField(default=False)
    lactose = models.BooleanField(default=False)

    halal = models.BooleanField(default=False)
    kosher = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)

    location = models.CharField(max_length=100, default="none")

    # perspective of staff adding a new meal to the database

    # change to location from other model