from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_ticket, name='book_ticket'),
    path('confirm/<int:booking_id>/', views.booking_confirm, name='booking_confirm'),
    path('history/', views.booking_history, name='booking_history'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
