from django.urls import path

from . import views

urlpatterns = [
    path('staffPage/', views.staffPage, name='staffPage')
]