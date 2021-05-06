from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.models import User
from mealPlan.forms import mealPlanForm
from .models import Meal
from findLocation.models import Origin, GoogleMapsResponse
from accounts.models import Profile, Student, MealPlan


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
# class StaffPageLoadWithLocations(TestCase):
#     def setUp(self):
#         newOrigin = Origin(origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213,
#                            longitude=-76.7143524)
#         newOrigin.save()
#         c = Client()
#         destinationList = ['Elkridge, MD', 'Towson, MD', 'Columbia, MD']
#         for i in destinationList:
#             c.post('/findLocation/addLocation/',
#                    {'destination': i, 'school': 'y', 'bus': 'n', 'timeframe': 'M\W', "remove": 'a'})
#
#     # test findLocation page works
#     def test_page_load(self):
#         # access staffPage page
#         response = self.client.get('/mealPlan/staffPage/')
#         # verify site status code (HTTP 200 OK)
#         self.assertEqual(response.status_code, 200)
#         # verify index.html is being used
#         self.assertTemplateUsed(response, template_name='mealPlan/staffpage.html')
#
#     def test_adding_locations(self):
#         # access staffPage page
#         response = self.client.get('/mealPlan/staffPage/')
#         results = response.context['googlemapsresult']
#         destinationList = ['Elkridge, MD', 'Towson, MD', 'Columbia, MD']
#         for location in destinationList:
#             num = results.filter(location=location).exists
#             self.assertTrue(num)

class StaffPageViewAndConfirmMealPlans(TestCase):
    def setUp(self):
        username = "admin"; email = "myemail@test.com"; password = "admin";
        reg_username = "user"; reg_password = "user";

        User.objects.create_superuser(username, email, password)
        admin = User.objects.get(username=username)
        admin.first_name, admin.last_name = 'admin', 'user'
        admin.save()
        profile = Profile(user=admin, address='1000 Hilltop Cir', city='Baltimore', state='MD', zip='21250',
                          district='Baltimore County')
        profile.save()

        origin = Origin(user=admin, origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213,
                        longitude=-76.7143524)
        origin.save()
        # print("Set origin for findLocation")

        User.objects.create_user(reg_username, email, reg_password)
        reg_user = User.objects.get(username=reg_username)
        reg_user.first_name, reg_user.last_name = 'TesingUser123', 'User'
        reg_user.save()
        profile = Profile(user=reg_user, address='1000 Hilltop Cir', city='Baltimore', state='MD', zip='21250',
                          district='Baltimore County')
        profile.save()

        origin = Origin(user=reg_user, origin='1000 Hilltop Cir, Baltimore, MD 21250, USA', latitude=39.2537213,
                        longitude=-76.7143524)
        origin.save()
        student = Student(user_account=profile, first_name="Billy", last_name="Bob", age=7, grade=8,
                          school="Catonsville High", student_id="AB04576",
                          allergic_celiac="No", allergic_shellfish="Yes", allergic_lactose="No",
                          preference_halal="Yes", preference_kosher="Yes", preference_vegetarian="No")
        student.save()
        mealplan = MealPlan(student_profile=student, pickup_type='Bus Stop', time='11:00am-11:10am', day='Monday/Wednesday', meal_breakfast='Yes', meal_lunch='No',
                            meal_dinner='No', pickup_location="Westland Gardens Apartments: 2.0 miles in 5 mins (11:00am-12:30pm)", complete="Yes")
        mealplan.save()
        # login as admin
        self.client.post('/accounts/login/', data={
            'username': 'admin',
            'password': 'admin',
        }, follow=True)

    # test findLocation page works
    def test_page_load(self):
        # access staffPage page
        response = self.client.get('/mealPlan/staffPage/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify index.html is being used
        self.assertTemplateUsed(response, template_name='mealPlan/staffpage.html')
        # verify that meal plan content appears on page
        self.assertContains(response, "TesingUser123")
        self.assertContains(response, "Westland Gardens Apartments: 2.0 miles in 5 mins (11:00am-12:30pm)")

    def test_confirm(self):
        # confirm student meal to send notification to correct user
        self.client.post('/mealPlan/send_confirm_notif/', data={
            'mealPk': '1'
        }, follow=True)
        # login as regular user
        self.client.post('/accounts/login/', data={
            'username': 'user',
            'password': 'user',
        }, follow=True)
        response = self.client.get('/notifs/inbox/')
        self.assertEqual(response.status_code, 200)
        # verify inbox.html is being used
        self.assertTemplateUsed(response, template_name='registration/inbox.html')
        # verify that the user was sent a notification about their meal plan
        self.assertContains(response, "Meal Plan Update!")
        self.assertContains(response, "Billy Bob&#x27;s meal is ready for pick up at Westland Gardens Apartments!")
        self.assertContains(response, "Click here for more information about this meal plan!")

