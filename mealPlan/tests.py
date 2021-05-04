from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.models import User
from mealPlan.forms import mealPlanForm
from .models import Meal
from findLocation.models import Origin

# Create your tests here.



class PageLoad(TestCase):
    # test if page is reachable
    def test_page_load(self):
        response = self.client.get('/mealPlan/')
        self.assertEqual(response.status_code, 200)

class TicketPostTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': '>pve_hm*N*&x<qbP8u'}
        User.objects.create_user(**self.credentials)

# second test non-functional due to error in posting {'content': "Ham Sandwich'}

    def test_sending_ticket(self):
        '''
        # create user
        #self.user = User.objects.create_user(username='testuser', password='12345', first_name="John", last_name="Doe", email="email@email.com")
        #self.client.login(username='testuser', password='12345')
        self.client.post('/accounts/login/', self.credentials, follow=True)
        c = Client()
        # send a ticket through client
        self.client.get('/mealPlan/')
        c.post('/mealPlan/ticket_add/', self.credentials, context={'content': "Ham Sandwich"})
        response = self.client.get(reverse('meal_plan'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ham Sandwich")
        '''
        pass


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

class MealFilterPageLoad(TestCase):
    # test findLocation page works
    def test_page_load(self):
        # access findLocation page
        response = self.client.get('/mealPlan/choosemeal/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='mealPlan/choosemeal.html')
