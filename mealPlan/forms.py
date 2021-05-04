from django import forms
from mealPlan.models import Meal


class mealPlanForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "New Meal Name"}))

    celiac = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    shellfish = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    lactose = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    halal = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    kosher = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    vegetarian = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    location = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Meal
        fields = ('content',)