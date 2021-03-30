from django.test import TestCase, Client
from django.urls import reverse

from .models import Destinations


# Create your tests here.
class PageLoad(TestCase):
    # test findLocation page works
    def test_page_load(self):
        # access findLocation page
        response = self.client.get('/findLocation/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='findLocation/index.html')


def create_destination(destination_text):
    """
    Create a destination with the given `destination_text`.
    """
    return Destinations.objects.create(text=destination_text)


class DestinationIndexViewTest(TestCase):
    def test_adding_destination(self):
        """
        Make sure that a destination inputted is on the page.
        """
        create_destination(destination_text="Elkridge, Maryland")
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Elkridge, Maryland")
