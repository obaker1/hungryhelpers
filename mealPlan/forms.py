from django import forms
from mealPlan.models import Post


class mealPlanForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ticket Content"}))

    class Meta:
        model = Post
        fields = ('post',)