from django import forms
from .models import Train, Schedule

class TrainSearchForm(forms.Form):
    source = forms.CharField(max_length=100, required=True)
    destination = forms.CharField(max_length=100, required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
