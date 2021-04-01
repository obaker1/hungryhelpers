from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db import models


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