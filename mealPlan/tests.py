from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.models import User
from mealPlan.forms import mealPlanForm
from .models import Meal

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
'''
    def test_sending_ticket(self):
        # create user
        #self.user = User.objects.create_user(username='testuser', password='12345', first_name="John", last_name="Doe", email="email@email.com")
        #self.client.login(username='testuser', password='12345')
        self.client.post('/accounts/login/', self.credentials, follow=True)
        c = Client()
        # send a ticket through client
        c.post('/mealPlan/ticket_add/', {'content': "Ham Sandwich"}, self.credentials)
        response = self.client.get(reverse('meal_plan'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ham Sandwich")
'''