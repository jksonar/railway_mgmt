from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Passenger
from .forms import BookingForm, PassengerForm
from trains.models import Schedule
from seats.models import Seat, SeatAvailability
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils import timezone

@login_required
def book_ticket(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            count = form.cleaned_data['passengers_count']
            train = schedule.train

            # Find available seats
            available_seats = SeatAvailability.objects.filter(
                train=train, schedule=schedule, status='Available'
            )[:count]

            if available_seats.count() < count:
                return render(request, 'bookings/book_ticket.html', {
                    'form': form,
                    'error': 'Not enough available seats.'
                })

            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                train=train,
                schedule=schedule,
                status='Confirmed'
            )

            PassengerFormSet = modelformset_factory(Passenger, form=PassengerForm, extra=count)

            if 'formset_submitted' in request.POST:
                formset = PassengerFormSet(request.POST, queryset=Passenger.objects.none())
                if formset.is_valid():
                    for form, seat_avail in zip(formset.forms, available_seats):
                        passenger = form.save(commit=False)
                        passenger.booking = booking
                        passenger.seat = seat_avail.seat
                        passenger.save()

                        # Mark seat as booked
                        seat_avail.status = 'Booked'
                        seat_avail.save()

                    return redirect('booking_confirm', booking_id=booking.id)
            else:
                formset = PassengerFormSet(queryset=Passenger.objects.none())
                return render(request, 'bookings/passenger_details.html', {
                    'formset': formset,
                    'booking': booking,
                    'formset_submitted': True
                })

    else:
        form = BookingForm()

    return render(request, 'bookings/book_ticket.html', {'form': form})


@login_required
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_confirm.html', {'booking': booking})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status != 'Cancelled':
        booking.status = 'Cancelled'
        booking.save()

        # Release seats
        for passenger in booking.passengers.all():
            seat = passenger.seat
            if seat:
                SeatAvailability.objects.filter(
                    train=booking.train,
                    schedule=booking.schedule,
                    seat=seat
                ).update(status='Available')

    return redirect('booking_history')
