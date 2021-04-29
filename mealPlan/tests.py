from django.test import TestCase
from accounts.models import Student

class PageLoad(TestCase):
    # test findLocation page works
    def test_page_load(self):
        # access findLocation page
        response = self.client.get('/mealPlan/choosemeal/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='mealPlan/choosemeal.html')

