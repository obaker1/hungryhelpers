from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.models import User
from mealPlan.forms import mealPlanForm
from .models import Meal
from findLocation.models import Origin, GoogleMapsResponse
from accounts.models import Profile


# Create your tests here.


class PageLoad(TestCase):
    # test if page is reachable
    def test_page_load(self):
        response = self.client.get('/mealPlan/')
        self.assertEqual(response.status_code, 200)


class TicketPostTest(TestCase):
    def setUp(self):
        # create user
        self.username = 'admin'
        self.first_name = 'admin'
        self.last_name = 'user'
        self.email = 'tester@test.com'
        self.password = '>pve_hm*N*&x<qbP8u'

        User.objects.create_superuser(self.username, self.email, self.password)
        admin = User.objects.get(username=self.username)
        admin = User.objects.get(username=self.username)
        profile = Profile(user=admin, address='1000 Hilltop Cir', city='Baltimore', state='MD', zip='21250',
                          district='Baltimore County')

    def test_send_ticket(self):
        # login
        # response = self.client.post('/accounts/login/', data={
        #     'username': self.username,
        #     'password': self.password,
        # }, follow=True)
        c = Client()

        # send a ticket through client
        c.post('/mealPlan/', context={'content': "Ham Sandwich"}, follow=True)
        response = self.client.get(reverse('meal_plan'))
        self.assertEqual(response.status_code, 200)

        # check if meal was added
        meal_added = Meal.objects.filter(content="Ham Sandwich")
        for meal in meal_added:
            self.assertEqual(meal.content, "Ham Sandwich")

    def test_send_complex_ticket(self):
        # login

        # response = self.client.post('/accounts/login/', data={
        #     'username': self.username,
        #     'password': self.password,
        # }, follow=True)
        c = Client()

        # send a ticket with more fields through client
        c.post('/mealPlan/', context={'content': "Carrot", 'location': GoogleMapsResponse(location="Catonsville High"),
                                                        "Vegetarian": True}, follow=True)
        response = self.client.get(reverse('meal_plan'))
        self.assertEqual(response.status_code, 200)

        # check if meal has all attributes that were sent
        meal_added = Meal.objects.filter(content="Carrot")
        for meal in meal_added:
            self.assertEqual(meal.content, "Carrot")
            self.assertEqual(meal.location.location, "Catonsville High")
            self.assertTrue(meal.vegetarian)


# Create your tests here.
class StaffPageLoadWithLocations(TestCase):
    def setUp(self):
        newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213,
                           longitude=-76.7143524)
        newOrigin.save()
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
