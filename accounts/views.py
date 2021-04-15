from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from .forms import EditSettingsForm, CreateProfileForm, EditProfileForm, StudentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Student
from django.shortcuts import render, get_object_or_404

class SignUpView(generic.CreateView):
    # Utilizes the built-in UserCreationForm
    form_class = UserCreationForm
    # Redirects user to login page upon successful registration
    template_name = 'registration/signup.html'
    #success_url = reverse_lazy('create_profile')
    success_url = '/create_profile'

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('create_profile'))

class EditSettingsView(LoginRequiredMixin, generic.UpdateView):
    # if user attempts to access settings page without logging in,
    # user will be redirected to the login page
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    # Utilizes custom data change form
    form_class = EditSettingsForm
    template_name = 'registration/edit_settings.html'
    # Redirects user to login page upon successful setting update
    success_url = reverse_lazy('home')
    # setting page will be unique to each user
    def get_object(self):
        return self.request.user

class ShowProfileView(DetailView):
    model = Profile
    template_name = 'registration/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context

class EditProfileView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    form_class = EditProfileForm
    #success_url = reverse_lazy('home')
    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.kwargs['pk']})

class CreateProfileView(CreateView):
    model = Profile
    template_name = "registration/create_profile.html"
    form_class = CreateProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AddStudentView(CreateView):
    model = Student
    template_name = "registration/add_student.html"
    form_class = StudentForm

    def form_valid(self, form):
        form.instance.user_account_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.kwargs['pk']})

class EditStudentView(UpdateView):
    model = Student
    template_name = 'registration/edit_student.html'
    form_class = StudentForm
    success_url = reverse_lazy('intermediate')

class DeleteStudentView(DeleteView):
    model = Student
    template_name = 'registration/delete_student.html'
    form_class = StudentForm
    success_url = reverse_lazy('intermediate')

def Intermediate(request):
    return render(request, 'registration/intermediate.html')
