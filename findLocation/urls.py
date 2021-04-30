from django.urls import path

from . import views

urlpatterns = [
    path('', views.findlocation, name='findlocation'),
    path('addLocation/', views.addLocation, name='addLocation'),
    path('addOrigin/', views.addOrigin, name='addOrigin'),
    path('addMore/', views.addMore, name='addMore'),
]