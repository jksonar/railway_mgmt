from django import forms
from trains.models import Schedule
from .models import Coach

class SeatAvailabilitySearchForm(forms.Form):
    schedule = forms.ModelChoiceField(queryset=Schedule.objects.all(), required=True)
    class_type = forms.ChoiceField(choices=Coach.CLASS_CHOICES)
