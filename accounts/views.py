from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    # Utilizes the built-in UserCreationForm
    form_class = UserCreationForm
    # Redirects user to login page upon successful registration
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'