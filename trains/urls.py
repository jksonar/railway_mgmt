from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.train_list, name='train_list'),
    path('search/', views.search_trains, name='search_trains'),
]
