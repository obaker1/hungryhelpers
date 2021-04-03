from django import forms
from django.forms import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Student

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
        fields = ('firstName', 'lastName', 'age', 'address', 'city', 'state', 'country', 'zip', 'school', 'grade', 'student_id')

        #name = forms.TextInput(attrs={'class': 'form-control'}),
        #age = forms.ChoiceField(label='', choices=AGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

        #widgets = {
            #'name': forms.TextInput(attrs={'class': 'form-control'}),
            #'age': forms.ChoiceField(attrs={'class': 'form-control'}, choices=AGE_CHOICES),

        #}