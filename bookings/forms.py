from django import forms
from .models import Passenger
from trains.models import Schedule
from seats.models import Seat

class BookingForm(forms.Form):
    schedule = forms.ModelChoiceField(queryset=Schedule.objects.all())
    passengers_count = forms.IntegerField(min_value=1, max_value=6)


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender']
