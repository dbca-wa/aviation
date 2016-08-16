from django.contrib import admin
from avs.models import *

class AVSBaseLookupModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id', 'name',)
    
admin.site.register(Task, AVSBaseLookupModelAdmin)
admin.site.register(Aircraft, AVSBaseLookupModelAdmin)

class PilotAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id','first_name','last_name',)
    
admin.site.register(Pilot, PilotAdmin)

class AircraftFlightLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight_log_number', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id', 'flight_log_number',)
    
admin.site.register(AircraftFlightLog, AircraftFlightLogAdmin)

class AircraftFlightLogDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id',)
    
admin.site.register(AircraftFlightLogDetail, AircraftFlightLogDetailAdmin)

class DutyTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'modified', 'modifier')
    date_hierarchy = 'created'
    search_fields = ('id',)
    
admin.site.register(DutyTime, DutyTimeAdmin)


