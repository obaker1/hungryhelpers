from django.urls import path
from .views import SignUpView, EditSettingsView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/', EditSettingsView.as_view(), name='edit_settings'),
]