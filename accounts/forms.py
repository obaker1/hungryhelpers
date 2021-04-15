from django import forms
from django.forms import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Student
from localflavor.us.us_states import STATE_CHOICES
import json

class EditSettingsForm(UserChangeForm):
    # Custom form requests only relevant information provided by the form.as_p packaged form
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = None
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            )

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('caretaker_names',)
        #fields = ()

        widgets = {
            'caretaker_names': HiddenInput(),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('caretaker_names',)

        widgets = {
            'caretaker_names': forms.Textarea(attrs={'class': 'form-control'}),
        }

class StudentForm(forms.ModelForm):

    class Meta:
        AGE_CHOICES = [(i, i) for i in range(11, 19)]
        GRADE_CHOICES = [(i, i) for i in range(6, 13)]
        SCHOOL_DISTRICTS = [
            ("Arbutus Middle", "Arbutus Middle"),
            ("Catonsville High", "Catonsville High"),
            ("Catonsville Middle", "Catonsville Middle"),
            ("Chesapeake High", "Chesapeake High"),
            ("Deep Creek Middle", "Deep Creek Middle"),
        ]

        model = Student
        fields = ('first_name', 'last_name', 'age', 'address', 'city', 'state', 'zip', 'school', 'grade', 'student_id', 'district_choice',
                  'allergic_celiac', 'allergic_shellfish', 'allergic_lactose', 'preference_halal', 'preference_kosher', 'preference_vegetarian', 'meal_breakfast', 'meal_lunch', 'meal_dinner')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.Select(attrs={'class': 'form-control'}, choices=AGE_CHOICES),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}, choices=STATE_CHOICES),
            'zip': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}, choices=SCHOOL_DISTRICTS),
            'grade': forms.Select(attrs={'class': 'form-control'}, choices=GRADE_CHOICES),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'district_choice': forms.TextInput(attrs={'class': 'form-control'}),

            'allergic_celiac': forms.TextInput(),
            'allergic_shellfish': forms.TextInput(),
            'allergic_lactose': forms.TextInput(),

            'preference_halal': forms.TextInput(),
            'preference_kosher': forms.TextInput(),
            'preference_vegetarian': forms.TextInput(),

            'meal_breakfast': forms.TextInput(),
            'meal_lunch': forms.TextInput(),
            'meal_dinner': forms.TextInput(),

        }