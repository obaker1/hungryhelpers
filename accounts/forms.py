from django import forms
from django.forms import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Student
from localflavor.us.us_states import STATE_CHOICES
from .static_info import AGE_CHOICES, GRADE_CHOICES, DISTRICTS, SCHOOLS

class CreateAccountForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            )

class EditSettingsForm(UserChangeForm):
    # Custom form requests only relevant information provided by the form.as_p packaged form
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    #first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = None
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            #'first_name',
            #'last_name',
            )

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'address', 'city', 'state', 'zip', 'district',)
        #fields = ()

        widgets = {
            #'caretaker_names': HiddenInput(),
            'first_name': HiddenInput(),
            'last_name': HiddenInput(),
            'address': HiddenInput(),
            'city': HiddenInput(),
            'state': HiddenInput(),
            'zip': HiddenInput(),
            'district': HiddenInput(),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'address', 'city', 'state', 'zip', 'district',)

        widgets = {
            #'caretaker_names': forms.Textarea(attrs={'class': 'form-control'}),\
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}, choices=STATE_CHOICES),
            'zip': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}, choices=DISTRICTS),
        }

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'age', 'grade', 'school', 'student_id',
                  'allergic_celiac', 'allergic_shellfish', 'allergic_lactose',
                  'preference_halal', 'preference_kosher', 'preference_vegetarian',)
                  #'meal_breakfast', 'meal_lunch', 'meal_dinner')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),

            'grade': forms.Select(attrs={'class': 'form-control'}, choices=GRADE_CHOICES),
            'age': forms.Select(attrs={'class': 'form-control'}, choices=AGE_CHOICES),
            'school': forms.Select(attrs={'class': 'form-control'}, choices=SCHOOLS),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),

            'allergic_celiac': forms.TextInput(),
            'allergic_shellfish': forms.TextInput(),
            'allergic_lactose': forms.TextInput(),

            'preference_halal': forms.TextInput(),
            'preference_kosher': forms.TextInput(),
            'preference_vegetarian': forms.TextInput(),

            # 'meal_breakfast': forms.TextInput(),
            # 'meal_lunch': forms.TextInput(),
            # 'meal_dinner': forms.TextInput(),
        }