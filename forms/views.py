from django.views.generic import UpdateView
from models import Person
from forms import PersonForm
from django.shortcuts import render

def index(request):
    return render(request, 'forms/people/person_form.html', context={})

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'people/person_update_form.html'
