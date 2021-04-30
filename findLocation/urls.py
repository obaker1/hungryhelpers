from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.findlocation, name='findlocation'),
    path('addLocation/', views.addLocation, name='addLocation'),
    path('addOrigin/', views.addOrigin, name='addOrigin'),
    url(r'^export-xls/$', views.export, name='export'),
    path('addMore/', views.addMore, name='addMore'),
]