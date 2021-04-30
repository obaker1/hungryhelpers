from django import forms
from mealPlan.models import Meal#, Choices
'''
RESTRICTIONS =[
    ("1", "Celiac"),
    ("2", "Shellfish"),
    ("3", "Lactose"),
    ("4", "Halal"),
    ("5", "Kosher"),
    ("6", "Vegetarian")
]
'''

#LOCATIONS = ["Baltimore", "Columbia", "Towson"]

class mealPlanForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Meal Plan"}))
    #restrictions = forms.BooleanField()

    celiac = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    shellfish = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    lactose = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    halal = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    kosher = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    vegetarian = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    #location = forms.CharField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}, choices=LOCATIONS))

    class Meta:
        model = Meal
        fields = ('content',)