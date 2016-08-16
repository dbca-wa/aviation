from restless.abstract2 import Audit, models
from django.contrib.auth.models import User
from datetime import datetime

#before remove activity and task
class ActiveModel(Audit):   
    effective_from = models.DateTimeField(default=datetime.now())
    effective_to = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

class AVSBaseLookupModel(ActiveModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
       
    class Meta:
        abstract = True
        ordering = ['name', ]
    
    def __unicode__(self):
        return self.name
        
class Task(AVSBaseLookupModel):
    pass
    @models.permalink
    def get_absolute_url(self):
        return ('taskupdate', [str(self.id)])
    
class Aircraft(AVSBaseLookupModel):
    pass
    @models.permalink
    def get_absolute_url(self):
        return ('aircraftupdate', [str(self.id)])

class Pilot(ActiveModel):
    '''
    Add some additional docstring info here later.
    '''
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    code = models.CharField(max_length = 3, unique=True)
    #user = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__ (self):
        return self.first_name + ' ' + self.last_name
    @models.permalink
    def get_absolute_url(self):
        return ('pilotupdate', [str(self.id)])
        
class AircraftFlightLog(Audit):
    '''
    Add some additional docstring info here later.
    '''
    flight_log_number = models.CharField(max_length=20,unique=True)
    date = models.DateField()
    aircraft = models.ForeignKey(Aircraft)
    fire_danger_index = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    def __unicode__ (self):
        return unicode(self.flight_log_number)        
    @models.permalink
    def get_absolute_url(self):
        return ('aircraftflightlogdetailsadd', [str(self.id)])
    
        
class AircraftFlightLogDetail(Audit):
    '''
    Add some additional docstring info here later.
    '''
    datcon = models.DecimalField(max_digits=9, decimal_places=1)
    time_out = models.TimeField(help_text='GMT+8')
    landings = models.IntegerField(default=0)
    fire_number = models.CharField(max_length=50, null=True, blank=True)
    fuel_added = models.IntegerField(default=0)
    #task = models.ForeignKey(Task, null=True, blank=True)
    #activity_type = models.ForeignKey(ActivityType, null=True, blank=True)
    task = models.ForeignKey(Task, null=True, blank=True)
    job_number = models.CharField(max_length = 30, null=True, blank=True)
    pilot_in_command = models.ForeignKey(Pilot, related_name = 'pilot_in_command')
    pilot_in_command_under_supervision = models.ForeignKey(Pilot, null=True, blank=True)
    aircraft_flight_log = models.ForeignKey(AircraftFlightLog)
    
    def __unicode__ (self):
        #return unicode(self.aircraft_flight_log) + ' - ' + self.id))
        return unicode(self.id)        

  
class DutyTime(Audit):
    
    date = models.DateField()
    pilot = models.ForeignKey(Pilot)
    datetime_on_first = models.TimeField(null=True, blank=True)
    datetime_off_first = models.TimeField(null=True, blank=True)    
    travel_km = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)    
    
    #class Meta:
        #unique_together = (("pilot", "date"),)    
    def __unicode__ (self):
        return unicode(self.remarks)
    @models.permalink
    def get_absolute_url(self):
        return ('dutytimeaddset', [str(self.pilot.id)])
    
   
