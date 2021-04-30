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
    # get all content from Post objects
    meals = Meal.objects.all()
    # filter to only content for user that is currently logged in
    #cur_posts = Post.objects.filter(user=request.user)
    # get all location objects

    args = {'form': form, 'meals': meals}
    #args = {'form': form, 'posts': posts, 'cur_posts': cur_posts}

    return render(request, 'mealPlan/index.html', args)


def ticket_add(request):
    # create post object using content from form and save
    meal_text = request.POST['content']

    #celiac = request.POST['celiac']
    #shellfish = request.POST['shellfish']
    #lactose = request.POST['lactose']

    #halal = request.POST['halal']
    #kosher = request.POST['kosher']
    #vegetarian = request.POST['vegetarian']

    #meal_restrictions = request.POST['restrictions']

    #new_meal = Meal(content=meal_text, user=request.user, celiac=celiac, shellfish=shellfish, lactose=lactose, halal=halal, kosher=kosher, vegetarian=vegetarian)
    new_meal = Meal(content=meal_text, user=request.user)
    new_meal.save()
    #new_meal.restrictions.set(meal_restrictions)
    return HttpResponseRedirect(reverse('meal_plan'))
    #return HttpResponseRedirect(reverse(mealPlanView.template_name))


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

