from django.db import models

class Train(models.Model):
    TRAIN_TYPES = [
        ('Express', 'Express'),
        ('Superfast', 'Superfast'),
        ('Passenger', 'Passenger'),
        ('Intercity', 'Intercity'),
    ]

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    train_type = models.CharField(max_length=20, choices=TRAIN_TYPES)

    def __str__(self):
        return f"{self.name} ({self.number})"


class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    station_name = models.CharField(max_length=100)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['stop_number']

    def __str__(self):
        return f"{self.train.name} - {self.station_name}"


class Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    def __str__(self):
        return f"{self.train.name} on {self.date}"
