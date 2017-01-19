from django.contrib.admin import register, ModelAdmin
from avs.models import (
    Task, Aircraft, Pilot, AircraftFlightLog, AircraftFlightLogDetail, DutyTime)


@register(Task)
class TaskAdmin(ModelAdmin):
    list_display = ('id', 'name', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id', 'name',)


@register(Aircraft)
class AircraftAdmin(ModelAdmin):
    list_display = ('id', 'name', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id', 'name',)


@register(Pilot)
class PilotAdmin(ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id', 'first_name', 'last_name',)


@register(AircraftFlightLog)
class AircraftFlightLogAdmin(ModelAdmin):
    list_display = ('id', 'flight_log_number', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id', 'flight_log_number',)


@register(AircraftFlightLogDetail)
class AircraftFlightLogDetailAdmin(ModelAdmin):
    list_display = ('id', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id',)


@register(DutyTime)
class DutyTimeAdmin(ModelAdmin):
    list_display = ('id', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id',)
