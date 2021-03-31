from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings

from .models import Destinations
from .models import GoogleMapsResponse


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
        Make sure that a destination inputted is in the database.
        """
        create_destination(destination_text="Towson, Maryland")
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Towson,")

    # def test_order_of_locations(self):
    #     """
    #     makes sure that all locations in the database are ordered
    #     correctly by distance (not by time)
    #     """

    def test_google_matrix_api(self):
        """
        makes sure that distance matrix API is working
        """
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?callback=initMap&libraries=&v=weekly&units=imperial'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_google_geocode_api(self):
        """
        makes sure that geocode API is working
        """
        url = 'https://maps.googleapis.com/maps/api/js?'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

