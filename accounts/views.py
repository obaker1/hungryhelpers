from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from .forms import EditSettingsForm, CreateProfileForm, EditProfileForm, StudentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Student
from django.contrib.auth import (get_user_model)


UserModel = get_user_model()

class SignUpView(generic.CreateView):
    # Utilizes the built-in UserCreationForm
    form_class = UserCreationForm
    # Redirects user to login page upon successful registration
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the user's information
        email = self.request.POST['email']
        username = self.request.POST['username']
        password = self.request.POST['password1']
        first_name = self.request.POST['firstName']
        last_name = self.request.POST['lastName']
        phone_number = self.request.POST['phone']
        address = self.request.POST['address']
        city = self.request.POST['city']
        state = self.request.POST['state']
        zip = self.request.POST['zip']
        district = self.request.POST['district']
        school = self.request.POST['school']
        student_name = self.request.POST['studentName']
        age = self.request.POST['age']
        grade = self.request.POST['grade']
        student_id = self.request.POST['studentID']

        # authenticates user then logs in
        user = authenticate(email = email, username=username, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, city=city, state=state, zip=zip, district=district, school=school)
        login(self.request, user)
        # automatically creates profile upon registration
        profile = Profile(user=user)
        profile.save()
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
    success_url = reverse_lazy('show_profile')

    def get_object(self):
        return self.request.user.profile

class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = "registration/create_profile.html"
    form_class = CreateProfileForm

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)

class AddStudentView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = "registration/add_student.html"
    form_class = StudentForm

    def form_valid(self, form):
        form.instance.user_account_id = self.request.user.profile.pk
        return super().form_valid(form)

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