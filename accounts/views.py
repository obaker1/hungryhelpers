from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import EditSettingsForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(generic.CreateView):
    # Utilizes the built-in UserCreationForm
    form_class = UserCreationForm
    # Redirects user to login page upon successful registration
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

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

