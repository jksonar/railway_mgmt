from django.shortcuts import render
from .models import Train, Schedule
from .forms import TrainSearchForm
from django.utils.timezone import datetime

def train_list(request):
    trains = Train.objects.all()
    return render(request, 'trains/train_list.html', {'trains': trains})


def search_trains(request):
    form = TrainSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        date = form.cleaned_data['date']

        results = Schedule.objects.filter(
            train__source__icontains=source,
            train__destination__icontains=destination,
            date=date
        ).select_related('train')

    return render(request, 'trains/search_results.html', {'form': form, 'results': results})
