from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Student

from findLocation.models import GoogleMapsResponse


# Create your tests here.
class StaffPageLoadWithLocations(TestCase):
    def setUp(self):
        c = Client()
        destinationList = ['Elkridge, MD', 'Towson, MD', 'Columbia, MD']
        for i in destinationList:
            c.post('/findLocation/addLocation/',
                   {'destination': i, 'school': 'y', 'bus': 'n', 'timeframe': 'M\W', "remove": 'a'})

    # test findLocation page works
    def test_page_load(self):
        # access staffPage page
        response = self.client.get('/mealPlan/staffPage/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='mealPlan/staffpage.html')

    def test_adding_locations(self):
        # access staffPage page
        response = self.client.get('/mealPlan/staffPage/')
        results = response.context['googlemapsresult']
        destinationList = ['Elkridge, MD', 'Towson, MD', 'Columbia, MD']
        for location in destinationList:
            num = results.filter(location=location).exists
            self.assertTrue(num)

class MealFilterPageLoad(TestCase):
    # test findLocation page works
    def test_page_load(self):
        # access findLocation page
        response = self.client.get('/mealPlan/choosemeal/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='mealPlan/choosemeal.html')
