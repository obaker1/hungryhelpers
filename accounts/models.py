from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from localflavor.us.us_states import STATE_CHOICES
import json

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    caretaker_names = models.TextField(null=True, blank=True)
    #models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')

class Student(models.Model):
    AGE_CHOICES = [(i,i) for i in range(11,19)]
    GRADE_CHOICES = [(i, i) for i in range(6, 13)]
    SCHOOL_DISTRICTS = [
        ("Arbutus Middle", "Arbutus Middle"),
        ("Catonsville High", "Catonsville High"),
        ("Catonsville Middle", "Catonsville Middle"),
        ("Chesapeake High", "Chesapeake High"),
        ("Deep Creek Middle", "Deep Creek Middle"),
    ]

    user_account = models.ForeignKey(Profile, related_name="students", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(choices=AGE_CHOICES)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    zip = models.CharField(max_length=33, blank=True)
    school = models.CharField(max_length=255, choices=SCHOOL_DISTRICTS, blank=True)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    student_id = models.CharField(max_length=255, blank=True)
    district_choice = models.CharField(max_length=255, blank=True)

    allergic_celiac = models.CharField(max_length=255, null=True, default="No")
    allergic_shellfish = models.CharField(max_length=255, null=True, default="No")
    allergic_lactose = models.CharField(max_length=255, null=True, default="No")

    preference_halal = models.CharField(max_length=255, null=True, default="No")
    preference_kosher = models.CharField(max_length=255, null=True, default="No")
    preference_vegetarian = models.CharField(max_length=255, null=True, default="No")

    meal_breakfast = models.CharField(max_length=255, null=True, default="No")
    meal_lunch = models.CharField(max_length=255, null=True, default="No")
    meal_dinner = models.CharField(max_length=255, null=True, default="No")


    def __str__(self):
        return '%s' % (self.first_name)