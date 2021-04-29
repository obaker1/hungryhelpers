from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.models import User
from .models import Origin

from .models import GoogleMapsResponse


# Create your tests here.
class PageLoad(TestCase):
    # test findLocation page works
    def test_page_load(self):
        # access findLocation page
        newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213, longitude=-76.7143524)
        newOrigin.save()
        newDest = GoogleMapsResponse(location='Arbutus Middle', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest.save()
        response = self.client.get('/findLocation/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='findLocation/index.html')

class OriginIndexViewTest(TestCase):
    # test adding origin
    def test_adding_origin(self):
        c = Client()
        # put default origins and destinations
        newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213, longitude=-76.7143524)
        newOrigin.save()
        newDest = GoogleMapsResponse(location='Arbutus Middle', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest.save()
        c.post('/findLocation/addOrigin/', {'origin': 'baltimore, MD'})
        response = self.client.get(reverse('findlocation'))
        self.assertEqual(response.status_code, 200)

class DestinationIndexViewTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': '>pve_hm*N*&x<qbP8u'}
        User.objects.create_superuser(**self.credentials)
        # put default origins and destinations
        newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213, longitude=-76.7143524)
        newOrigin.save()
        newDest = GoogleMapsResponse(location='Arbutus Middle', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest.save()

    def test_adding_destination(self):
        """
        Make sure that a destination inputted is in the database.
        """
        self.client.post('/accounts/login/', self.credentials, follow=True)
        c = Client()
        c.post('/findLocation/addOrigin/', {'origin': 'baltimore, MD'})
        c.post('/findLocation/addLocation/', {'destination': 'Towson, Maryland', 'school': 'y', 'bus': 'n', 'timeframe': 'M\W', 'remove': 'a'})
        response = self.client.get(reverse('findlocation'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Towson,")

    def test_removing_destination(self):
        """
        Make sure that a destination is removed from the database.
        """
        c = Client()
        # adding a location
        c.post('/findLocation/addLocation/', {'destination': 'Towson, Maryland', 'school': 'y', 'bus': 'n', 'timeframe': 'M\W', "remove": 'a', 'origin': 'Towson MD'})
        # removing a location
        c.post('/findLocation/addLocation/', {'destination': 'Towson, Maryland', 'school': 'y', 'bus': 'n', 'timeframe': 'M\W', "remove": 'r', 'origin': 'Towson MD'})
        response = self.client.get(reverse('findlocation'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Towson,")

    def test_google_matrix_api(self):
        """
        makes sure that distance matrix API is working
        """
        params = {
            'key': settings.GOOGLE_MAPS_API_KEY,
            'origins': ['Columbia, MD'],
            'destinations': 'Towson, Maryland'
        }
        # calls distance matrix API
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?callback=initMap&libraries=&v=weekly&units=imperial'
        response = requests.get(url, params)
        origin_address = response.json()['origin_addresses'][0]
        self.assertIn('Columbia, MD', origin_address)
        self.assertEqual(response.status_code, 200)

    def test_google_geocode_api(self):
        """
        makes sure that geocode API is working
        """
        url = 'https://maps.googleapis.com/maps/api/js?'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

class TestOrdering(TestCase):
    def test_order_of_locations(self):
        """
        makes sure that all locations in the database are ordered
        correctly by distance (not by time)
        """
        c = Client()
        newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213, longitude=-76.7143524)
        newOrigin.save()
        destinationList = ['Elkridge, MD', 'Towson, MD', 'Columbia, MD' ]
        destinationListCorrect = ['Elkridge, MD', 'Columbia, MD', 'Towson, MD']
        for i in destinationList:
            c.post('/findLocation/addLocation/', {'destination': i, 'school': 'y', 'bus': 'n', 'timeframe': 'M\W', "remove": 'a', 'origin': 'Towson MD'})
            response = self.client.get(reverse('findlocation'))
        counter = 0
        googlemaps = GoogleMapsResponse.objects.all().order_by('distance', 'location')
        for destinations in googlemaps:
            self.assertIn(destinationListCorrect[counter], destinations.location)
            counter += 1

        self.assertEqual(response.status_code, 200)

class TestMoreLocations(TestCase):
    def test_show_more_locations(self):
        """
        Make sure page loads for showing 10 more locations
        """
        newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213, longitude=-76.7143524)
        newOrigin.save()
        newDest1 = GoogleMapsResponse(location='Arbutus Middle', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest1.save()
        newDest2 = GoogleMapsResponse(location='Arbutus Middl', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest2.save()
        newDest3 = GoogleMapsResponse(location='Arbutus Midd', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest3.save()
        newDest4 = GoogleMapsResponse(location='Arbutus Mid', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest4.save()
        newDest5 = GoogleMapsResponse(location='Arbutus Mi', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest5.save()
        newDest6 = GoogleMapsResponse(location='Arbutus M', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest6.save()
        newDest7 = GoogleMapsResponse(location='Arbutus ', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest7.save()
        newDest8 = GoogleMapsResponse(location='Arbutus', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest8.save()
        newDest9 = GoogleMapsResponse(location='Arbutu', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest9.save()
        newDest10 = GoogleMapsResponse(location='Arbut', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest10.save()
        newDest11 = GoogleMapsResponse(location='Arbu', distance='2.9', time='7 mins', bus='F', school='T', address='5525 Shelbourne Rd, Baltimore, MD 21227, USA', timeframe='M/W 11am-1pm', latitude='39.248289', longitude='-76.7057813')
        newDest11.save()
        response = self.client.get('/findLocation/addMore/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='findLocation/index.html')