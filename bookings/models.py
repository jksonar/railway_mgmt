from django.db import models
from django.contrib.auth.models import User
from trains.models import Train, Schedule
from seats.models import Seat

class Booking(models.Model):
    STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Confirmed')

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.status}"


class Passenger(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    seat = models.OneToOneField(Seat, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} (Seat {self.seat})"
