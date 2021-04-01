from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from notifications.signals import notify




# test if page is reachable
class PageLoad(TestCase):
    def test_page_load(self):
        response = self.client.get('/notifs/')
        self.assertEqual(response.status_code, 200)

# send notification and check if received by user
class NotifyTest(TestCase):
    def test_check_notif(self):
        # create new user and login
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        # specify user to send notif to
        user = User.objects.get(username='testuser')
        notify.send(user, recipient=user, verb='your order is ready for pickup!')
        # check if notif received
        response = self.client.get('/notifs/inbox/notifications/api/unread_list/?max=5 HTTP/1.1')
        self.assertEqual(response.status_code, 200)
