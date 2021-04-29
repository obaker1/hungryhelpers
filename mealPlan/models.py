from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    post = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    # attributes to add: allergies, preferences
    # user and location from other models
    # perspective of staff adding a new meal to the database

    #def __str__(self):
    #    return self.post