# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView
from mealPlan.forms import mealPlanForm, confirmPlan
from mealPlan.models import Meal
from accounts.models import Student, MealPlan
from findLocation.models import GoogleMapsResponse
from notifications.signals import notify


def meal_plan(request):
    form = mealPlanForm()
    # get all content from Meal objects
    meals = Meal.objects.all()

    googlemaps = GoogleMapsResponse.objects.all()

    args = {'form': form, 'meals': meals, 'googlemaps': googlemaps}

    return render(request, 'mealPlan/index.html', args)


def ticket_add(request):
    # create meal object using content from form and save
    meal_text = request.POST['content']

    restrictions = {'celiac': request.POST.get('Celiac', False), 'shellfish': request.POST.get('Shellfish', False),
                    'lactose': request.POST.get('Lactose', False), 'halal': request.POST.get('Halal', False),
                    'kosher': request.POST.get('Kosher', False), 'vegetarian': request.POST.get('Vegetarian', False)}

    for restriction in restrictions:
        if restrictions[restriction] == 'on':
            restrictions[restriction] = True

    location = int(request.POST.get("locations", "none"))
    location2 = GoogleMapsResponse.objects.get(id=location)

    new_meal = Meal(content=meal_text, celiac=restrictions['celiac'],
                    shellfish=restrictions['shellfish'], lactose=restrictions['lactose'],
                    halal=restrictions['halal'], kosher=restrictions['kosher'],
                    vegetarian=restrictions['vegetarian'], location=location2)

    new_meal.save()
    return HttpResponseRedirect(reverse('meal_plan'))

def sendConfirmNotif(request):
    mealPk = request.POST.get("mealPk", 0)
    print(mealPk)
    if mealPk != "none":
        sender = User.objects.get(username=request.user)
        mealObj = MealPlan.objects.get(id=mealPk)
        userPk = mealObj.student_profile.user_account.user.pk
        studObj = mealObj.student_profile
        receiver = User.objects.get(id=userPk)
        locationInfo = mealObj.pickup_location
        loc = locationInfo[:locationInfo.index(':')]
        #print(mealPk)
        notify.send(sender, recipient=receiver, verb=mealPk,
                    description=str(studObj.first_name) + " " + str(studObj.last_name) + "'s meal is ready for pick up at " + str(loc) + "!")
        return HttpResponseRedirect(reverse('staffPage'))

def staffPage(request):
    form = confirmPlan()
    mealplans = MealPlan.objects.all()
    #googlemaps = GoogleMapsResponse.objects.all()
    context={'mealplans': mealplans, 'form': form}
    return render(request, 'mealPlan/staffpage.html', context)

