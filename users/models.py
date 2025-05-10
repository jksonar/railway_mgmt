from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Passenger', 'Passenger'),
        ('Admin', 'Admin'),
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    id_proof = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Passenger')

    def __str__(self):
        return f"{self.user.username} Profile"
