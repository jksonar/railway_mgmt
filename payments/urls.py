from django.urls import path
from . import views

urlpatterns = [
    path('summary/<int:booking_id>/', views.payment_summary, name='payment_summary'),
    path('simulate/<int:booking_id>/<str:outcome>/', views.simulate_payment, name='simulate_payment'),
]
