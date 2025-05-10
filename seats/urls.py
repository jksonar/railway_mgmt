from django.urls import path
from . import views

urlpatterns = [
    path('availability/', views.seat_availability_view, name='seat_availability'),
]
