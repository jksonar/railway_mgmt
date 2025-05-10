from django.db import models
from trains.models import Train, Schedule

class Coach(models.Model):
    CLASS_CHOICES = [
        ('SL', 'Sleeper'),
        ('3A', 'AC 3 Tier'),
        ('2A', 'AC 2 Tier'),
        ('1A', 'AC First Class'),
        ('GEN', 'General'),
    ]

    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='coaches')
    coach_number = models.CharField(max_length=10)
    class_type = models.CharField(max_length=3, choices=CLASS_CHOICES)

    def __str__(self):
        return f"{self.train.name} - Coach {self.coach_number} ({self.class_type})"


class Seat(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.coach.coach_number} - Seat {self.seat_number}"


class SeatAvailability(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Booked', 'Booked'),
    )

    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.train.name} - {self.seat} ({self.status})"
