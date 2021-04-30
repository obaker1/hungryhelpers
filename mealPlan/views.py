# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView
from mealPlan.forms import mealPlanForm
from mealPlan.models import Meal


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
