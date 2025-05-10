from collections import defaultdict
from django.shortcuts import render
from .models import SeatAvailability, Seat, Coach
from .forms import SeatAvailabilitySearchForm

def seat_availability_view(request):
    form = SeatAvailabilitySearchForm(request.GET or None)
    availability = []

    if form.is_valid():
        schedule = form.cleaned_data['schedule']
        class_type = form.cleaned_data['class_type']

        availability = SeatAvailability.objects.filter(
            schedule=schedule,
            train=schedule.train,
            seat__coach__class_type=class_type
        ).select_related('seat', 'seat__coach')

    return render(request, 'seats/seat_availability.html', {
        'form': form,
        'availability': availability
    })

def seat_layout_view(request):
    form = SeatAvailabilitySearchForm(request.GET or None)
    seat_map = defaultdict(list)

    if form.is_valid():
        schedule = form.cleaned_data['schedule']
        class_type = form.cleaned_data['class_type']
        seats = SeatAvailability.objects.filter(
            schedule=schedule,
            train=schedule.train,
            seat__coach__class_type=class_type
        ).select_related('seat', 'seat__coach')

        for seat in seats:
            seat_map[seat.seat.coach.coach_number].append(seat)

    return render(request, 'seats/seat_layout.html', {
        'form': form,
        'seat_map': seat_map
    })
