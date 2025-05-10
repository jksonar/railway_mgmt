# from django.contrib import admin
# from .models import Train,Route,Schedule
# # Register your models here.

# admin.site.register(Train)
# admin.site.register(Route)
# admin.site.register(Schedule)

from django.contrib import admin
from .models import Train, Route, Schedule

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'source', 'destination')
    search_fields = ('name', 'number', 'source', 'destination')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('train', 'station_name', 'arrival_time', 'departure_time')
    list_filter = ('train',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('train', 'date', 'departure_time', 'arrival_time')
    list_filter = ('train', 'date')
