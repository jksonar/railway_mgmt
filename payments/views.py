from django.shortcuts import render, redirect, get_object_or_404
from bookings.models import Booking
from .models import Payment
from django.contrib import messages

def payment_summary(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Example fare calculation
    base_fare = 100  # Replace with real logic
    total_passengers = booking.passenger_set.count()
    total_amount = base_fare * total_passengers

    context = {
        'booking': booking,
        'amount': total_amount,
    }
    return render(request, 'payments/payment_summary.html', context)

def simulate_payment(request, booking_id, outcome):
    booking = get_object_or_404(Booking, id=booking_id)

    amount = 100 * booking.passenger_set.count()  # Same logic as above

    payment, created = Payment.objects.get_or_create(booking=booking, defaults={
        'amount': amount,
        'payment_method': 'card',
    })

    if outcome == 'success':
        payment.payment_status = 'success'
        messages.success(request, "Payment successful!")
    else:
        payment.payment_status = 'failed'
        messages.error(request, "Payment failed!")

    payment.save()

    return redirect('booking_detail', booking_id=booking.id)
