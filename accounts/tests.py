from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import StudentForm

class SignUpTest(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = '>pve_hm*N*&x<qbP8u'

    def test_signup_page(self):
        # access signup page
        response = self.client.get('/accounts/signup/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify signup.html is being used
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_form(self):
        # send signup data to page
        response = self.client.post('/accounts/signup/', data={
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        # check that a page redirection occurred (HTTP 302)
        self.assertEqual(response.status_code, 302)
        # check if account was successfully made
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)


class LogInTest(TestCase):
    def setUp(self):
        # valid credentials
        self.credentials = {
            'username': 'test',
            'password': '>pve_hm*N*&x<qbP8u'}
        # invalid credentials
        self.credentials2 = {
            'username': 'test',
            'password': '>pve_hm*N&x<qbP8u'
        }
        User.objects.create_user(**self.credentials)

    def test_login_page(self):
        # access signup page
        response = self.client.get('/accounts/login/')
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify signup.html is being used
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_login_success(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # check site redirection destination returns status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # check that the user successfully logged in
        self.assertTrue(response.context['user'].is_active)
        # check that the user has been redirected to home
        self.assertTemplateUsed(response, template_name='home.html')

    def test_login_fail(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials2, follow=True)
        # check site redirection destination returns status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # check that the user was unsuccessful when logging in
        self.assertFalse(response.context['user'].is_active)
        # check that the user is shown appropriate message
        self.assertTrue('Please enter a correct username and password' in str(response.content))


class LogOutTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': '>pve_hm*N*&x<qbP8u'}
        User.objects.create_user(**self.credentials)

    def test_logout_page(self):
        # access logout page
        response = self.client.get('/accounts/logout/')
        # verify site redirection status code (HTTP 302)
        self.assertEqual(response.status_code, 302)

        # re-access logout page and follow redirection
        response = self.client.get('/accounts/logout/', follow=True)
        # verify site redirection destination returns status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify home.html is being used
        self.assertTemplateUsed(response, template_name='home.html')

    def test_logout(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # check that a page redirection occurred (HTTP 302)
        self.assertEqual(response.status_code, 200)
        # check that the user successfully logged in
        self.assertTrue(response.context['user'].is_active)
        # check that the user has been redirected to home
        self.assertTemplateUsed(response, template_name='home.html')
        # request logout
        response = self.client.get("/accounts/logout/", follow=True)
        # check site status code (HTTP 200 OK)
        self.assertEquals(response.status_code, 200)
        # check user is no longer active
        self.assertFalse(response.context['user'].is_active)
        # check user is shown "You are not logged in" message
        self.assertTrue('You are not logged in' in str(response.content))

class EditSettingsTest(TestCase):
    def setUp(self):
        # valid credentials
        self.credentials = {
            'username': 'test',
            'password': '>pve_hm*N*&x<qbP8u'}
        User.objects.create_user(**self.credentials)

        # information for settings page
        self.username = 'test'
        self.email = 'tester@tset.com'
        self.first_name = 'testing'
        self.last_name = 'mctest'

    def test_settings_page_while_logged_out(self):
        # access settings page
        response = self.client.get('/accounts/settings/', follow=True)
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify a redirect was issued to take user to the login page
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_settings_page_while_logged_in(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # check site redirection destination returns status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # check that the user successfully logged in
        self.assertTrue(response.context['user'].is_active)
        # check that the user has been redirected to home
        self.assertTemplateUsed(response, template_name='home.html')
        # access settings page
        response = self.client.get('/accounts/settings/', follow=True)
        self.assertEqual(response.status_code, 200)
        # verify edit_settings.html is being used
        self.assertTemplateUsed(response, template_name='registration/edit_settings.html')
        # send and save information to settings page
        response = self.client.post('/accounts/settings/', data={
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name' : self.last_name
        }, follow=True)
        # check that the user has been redirected to home after updating settings
        self.assertTemplateUsed(response, template_name='home.html')
        # reaccess settings page
        response = self.client.get('/accounts/settings/')
        # verifies that the information has been successfully updated (username, email, fn, and ln)
        self.assertContains(response, self.username)
        self.assertContains(response, self.email)
        self.assertContains(response, self.first_name)
        self.assertContains(response, self.last_name)

class ProfileTest(TestCase):
    def setUp(self):
        # valid credentials

        self.username = 'test'
        self.password = '>pve_hm*N*&x<qbP8u'

        # information for add student page
        self.first_name = 'Billy'
        self.last_name = 'Manson'
        self.age = 11
        self.address = '1234 Test Street'
        self.city = 'Testingburg'
        self.state = 'Alaska'
        self.zip = '12345'
        self.school = 'Catonsville High'
        self.grade = 8
        self.student_id = 'AB04576'
        self.district_choice = '2nd Avenue and Francis Avenue'
        self.allergic_celiac = 'Yes'
        self.allergic_shellfish = 'No'
        self.allergic_lactose = 'Yes'
        self.preference_halal = 'Yes'
        self.preference_kosher = 'No'
        self.preference_vegetarian = 'No'
        self.meal_breakfast = 'No'
        self.meal_lunch = 'Yes'
        self.meal_dinner = 'No'
        self.err_msg = "You are either not logged in or do not have access to this profile."

    def test_profile_page(self):
        ### sign up and log into account
        # access and create account on signup page
        response = self.client.post('/accounts/signup/', data={
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        }, follow=True)
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # check if account was successfully made
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        # verify site status code (HTTP 200 OK)
        self.assertEqual(response.status_code, 200)
        # verify redirection was successfully made to home
        self.assertTemplateUsed(response, template_name='registration/create_profile.html')
        # click button that creates profile for user (done automatically in active testing)
        response = self.client.post('/accounts/create_profile/', follow=True)
        self.assertTemplateUsed(response, template_name='home.html')

        ### using the user id, access settings page and relevant data
        # access settings page
        response = self.client.get('/accounts/' + str(response.context['user'].pk) + '/profile/', follow=True)
        # verify correct template was used
        self.assertTemplateUsed(response, template_name='registration/profile.html')

        # access page that allows caretaker to add student
        response = self.client.get('/accounts/' + str(response.context['user'].pk) + '/add_student/', follow=True)
        # verify correct template was used
        self.assertTemplateUsed(response, template_name='registration/add_student.html')
        # enter data into form

        response = self.client.post('/accounts/' + str(response.context['user'].pk) + '/add_student/', data={
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'address': self.address,
            'city' : self.city,
            'state' : self.state,
            'zip' : self.zip,
            'school' : self.school,
            'grade' : self.grade,
            'student_id' : self.student_id,
            'district_choice' : self.district_choice,
            'allergic_celiac' : self.allergic_celiac,
            'allergic_shellfish' : self.allergic_shellfish,
            'allergic_lactose' : self.allergic_lactose,
            'preference_halal' : self.preference_halal,
            'preference_kosher' : self.preference_kosher,
            'preference_vegetarian' : self.preference_vegetarian,
            'meal_breakfast' :self.meal_breakfast,
            'meal_lunch' :self.meal_lunch,
            'meal_dinner' : self.meal_dinner,
        }, follow=True)

        # verify success of form submission
        self.assertEqual(response.status_code, 200)
        userPrimaryKey = response.context['user'].pk
        self.assertContains(response, self.age)
        self.assertContains(response, self.state)
        self.assertContains(response, self.student_id)
        self.assertContains(response, self.allergic_lactose)
        self.assertContains(response, self.meal_dinner)


        ### log out of user's current session and attempt to access same page based on primary key value
        response = self.client.get("/accounts/logout/", follow=True)
        # check site status code (HTTP 200 OK)
        self.assertEquals(response.status_code, 200)
        # check user is no longer active
        self.assertFalse(response.context['user'].is_active)
        # check user is shown "You are not logged in" message
        self.assertContains(response, 'You are not logged in')
        # attempt to access settings page
        response = self.client.get('/accounts/'+ str(userPrimaryKey) +'/profile/', follow=True)
        # verify that user is unable to view profile and is met with the appropriate message
        self.assertContains(response, self.err_msg)

        ### attempt to load a profile page that has never existed
        # attempt to access settings page
        response = self.client.get('/accounts/300/profile/', follow=True)
        # verify that user is met with a 404 site status code
        self.assertEqual(response.status_code, 404)

