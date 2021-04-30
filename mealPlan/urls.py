from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url
#from mealPlan.views import mealPlanView

urlpatterns = [
    #path('', mealPlanView.as_view(), name='index'),
    path('', views.meal_plan, name='meal_plan'),
    path('ticket_add/', views.ticket_add, name='ticket_add'),
    path('staffPage/', views.staffPage, name='staffPage'),
    path('choosemeal/', views.choosemeal, name='choosemeal'),
]