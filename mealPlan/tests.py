from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.models import User
from mealPlan.forms import mealPlanForm

# Create your tests here.



class PageLoad(TestCase):
    # test if page is reachable
    def test_page_load(self):
        response = self.client.get('/mealPlan/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='mealPlan/index.html')

class TicketPostTest(TestCase):
    def test_sending_ticket(self):
        # create user
        self.user = User.objects.create_user(username='testuser', password='12345', first_name="John", last_name="Doe", email="email@email.com")
        self.client.login(username='testuser', password='12345')
        c = Client()
        # send a ticket through client
        c.post('/mealPlan', {'form': mealPlanForm(), 'post': "I am very hungry"})
        response = self.client.get(reverse('mealPlan'))
        self.assertEqual(response.status_code, 200)