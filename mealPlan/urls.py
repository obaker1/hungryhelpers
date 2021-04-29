from django.urls import path

from . import views

urlpatterns = [
    path('choosemeal/', views.choosemeal, name='choosemeal')
]