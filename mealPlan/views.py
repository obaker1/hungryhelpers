# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView
from mealPlan.forms import mealPlanForm
from mealPlan.models import Meal
from accounts.models import Student
from findLocation.models import GoogleMapsResponse


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

    location = request.POST.get("locations", "none")

    new_meal = Meal(content=meal_text, user=request.user, celiac=restrictions['celiac'],
                    shellfish=restrictions['shellfish'], lactose=restrictions['lactose'],
                    halal=restrictions['halal'], kosher=restrictions['kosher'],
                    vegetarian=restrictions['vegetarian'], location=location)

    new_meal.save()
    return HttpResponseRedirect(reverse('meal_plan'))


def staffPage(request):
    googlemaps = GoogleMapsResponse.objects.all()
    context={'googlemapsresult': googlemaps}
    return render(request, 'mealPlan/staffpage.html', context)


def choosemeal(request):
    theMeal= ["Chicken, Rice, and Vegetables", "No", "Yes", "Yes" , "Yes", "Yes", "No", "No", "No", "Yes"]
    students = Student.objects.all()
    conflicts = []
    for i in students:
        newConflict = [[i.first_name],[]]

        if i.allergic_celiac == "Yes" and theMeal[1] == "No":
            newConflict[1].append("Celiac allergy Conflict")
        if i.allergic_shellfish == "Yes" and theMeal[2] == "No":
            newConflict[1].append("Shellfish allergy Conflict")
        if i.allergic_lactose == "Yes" and theMeal[3] == "No":
            newConflict[1].append("Lactose allergy Conflict")
        if i.preference_halal == "Yes" and theMeal[5] == "No":
            newConflict[1].append("Halal Conflict")
        if i.preference_kosher== "Yes" and theMeal[5] == "No":
            newConflict[1].append("Kosher Conflict")
        if i.preference_vegetarian == "Yes" and theMeal[6] == "No":
            newConflict[1].append("Vegetarian Conflict")
        if len(newConflict) > 1:
            conflicts.append(newConflict)
    print(conflicts)
    context={'theMeal': theMeal,
             'students': conflicts}
    return render(request, 'mealPlan/choosemeal.html', context)

