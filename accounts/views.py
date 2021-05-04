from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from .forms import EditSettingsForm, EditProfileForm, StudentForm, CreateAccountForm, MealPlanForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Student, MealPlan
from django.contrib.auth import (get_user_model)
from findLocation.models import Origin, GoogleMapsResponse
from findLocation.views import getLocations
from django.conf import settings
import json, math, requests


UserModel = get_user_model()

class SignUpView(generic.CreateView):
    # Utilizes the built-in UserCreationForm
    form_class = CreateAccountForm
    # Redirects user to login page upon successful registration
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        email = self.request.POST['email']
        password = self.request.POST['password1']
        # authenticates user then logs in
        user = authenticate(username=username, first_name=first_name, last_name=last_name, email=email,password=password)
        login(self.request, user)
        # automatically creates profile upon registration
        profile = Profile(user=user, address='', city='', state='', zip='', district='')
        profile.save()
        origin = Origin(user=user)
        origin.save()
        return HttpResponseRedirect(reverse_lazy('home'))

class EditSettingsView(LoginRequiredMixin, generic.UpdateView):
    # if user attempts to access settings page without logging in,
    # user will be redirected to the login page
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    # Utilizes custom data change form
    #fields = '__all__'
    form_class = EditSettingsForm
    template_name = 'registration/edit_settings.html'
    # Redirects user to login page upon successful setting update
    success_url = reverse_lazy('home')
    # setting page will be unique to each user
    def get_object(self):
        return self.request.user

class ShowProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'registration/profile.html'

    def get_object(self):
        return self.request.user.profile

class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    form_class = EditProfileForm
    #success_url = reverse_lazy('show_profile')

    def form_valid(self, form):
        self.object = form.save()
        locStr = form.instance.address + ", " + form.instance.city + ", " + form.instance.state + " " + form.instance.zip
        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

        params = {
            'key': settings.GOOGLE_MAPS_API_KEY,
            'address': locStr,
            'sensor': 'false',
        }
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        result = res['results'][0]
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        Origin.objects.filter(user=self.object.id).update(origin=locStr, latitude=lat, longitude=lng)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('show_profile')

    def get_object(self):
        return self.request.user.profile

# class CreateProfileView(LoginRequiredMixin, CreateView):
#     model = Profile
#     template_name = "registration/create_profile.html"
#     form_class = CreateProfileForm
#
#     def get_object(self):
#         return self.request.user
#
#     def form_valid(self, form):
#         return super().form_valid(form)

class AddStudentView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = "registration/add_student.html"
    form_class = StudentForm

    def form_valid(self, form):
        form.instance.user_account_id = self.request.user.profile.pk
        self.object = form.save()
        mealplan = MealPlan(student_profile=self.object, pickup_type='', time='', day='', meal_breakfast='', meal_lunch='', meal_dinner='')
        mealplan.save()
        #return super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('show_profile')

class EditStudentView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'registration/edit_student.html'
    form_class = StudentForm

    # Returns student query set to the appropriate authorized user
    # Unauthorized users will be met with a 404
    def get_queryset(self):
        base_qs = super(EditStudentView, self).get_queryset()
        return base_qs.filter(user_account=self.request.user.profile)

    def form_valid(self, form):
        # Extra security that prevents unauthorized users from being able to change/save student profile info
        if self.request.user.profile.pk == form.instance.user_account_id:
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy("home"))

    def get_success_url(self):
        return reverse_lazy('show_profile')

class DeleteStudentView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'registration/delete_student.html'
    form_class = StudentForm

    # Returns student query set to the appropriate authorized user
    # Unauthorized users will be met with a 404 error
    def get_queryset(self):
        base_qs = super(DeleteStudentView, self).get_queryset()
        return base_qs.filter(user_account=self.request.user.profile)

    def get_success_url(self):
        return reverse_lazy('show_profile')

class MealPlansView(LoginRequiredMixin, DetailView):
    model = MealPlan
    template_name = 'registration/meal_plans.html'

    def get_context_data(self, **kwargs):
        context = super(MealPlansView, self).get_context_data(**kwargs)
        mealObjs = {}
        for student in Student.objects.filter(user_account=self.request.user.profile):
            mealObjs[student.pk] = MealPlan.objects.get(id=student.pk)
            #print(obj.pickup_type)
            #mealObjs.append(student.pk)
        #print(studIDs)
        #print(mealObjs)
        context['mealplans'] = mealObjs #Student.objects.get(id=self.kwargs['pk'])
        return context

    def get_object(self):
        return self.request.user.profile

# class CreateMealPlanView(LoginRequiredMixin, CreateView):
#     model = MealPlan
#     template_name = "registration/create_meal_plan.html"
#     form_class = MealPlanForm
#
#     def form_valid(self, form):
#         #print(form.instance.student_profile_id)
#         #form.instance.student_profile_id = self.request.user.profile..pk
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('show_profile')
#
class EditMealPlanView(LoginRequiredMixin, UpdateView):
    model = MealPlan
    template_name = 'registration/edit_meal_plan.html'
    form_class = MealPlanForm

    # Returns student query set to the appropriate authorized user
    # Unauthorized users will be met with a 404
    def get_queryset(self, **kwargs):
        base_qs = super(EditMealPlanView, self).get_queryset()
        studpks = []
        for student in Student.objects.filter(user_account=self.request.user.profile):
            studpks.append(student.pk)
        if self.kwargs['pk'] in studpks:
            return base_qs.filter(student_profile=Student.objects.get(id=self.kwargs['pk']))
        raise Http404("Unauthorized access.")

    def get_context_data(self, **kwargs):
        context = super(EditMealPlanView, self).get_context_data(**kwargs)
        context['req_student'] = Student.objects.get(id=self.kwargs['pk'])

        origin = Origin.objects.get(id=self.request.user.id)
        result = getLocations(10, originObj=origin)
        #print(result)
        context['api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['origin'] = result[0]
        context['googlemapsresult'] = result[1]
        context['locationList'] = result[2]
        context['addressList'] = result[3]
        context['filter'] = result[4]

        return context

    def form_valid(self, form, **kwargs):
        self.object = form.save()
        return HttpResponseRedirect(self.request.path_info)

    def get_success_url(self):
        return reverse_lazy('edit_meal_plans', self.kwargs['pk'])