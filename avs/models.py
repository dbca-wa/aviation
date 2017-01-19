from __future__ import print_function, unicode_literals, absolute_import
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from datetime import datetime

from .base import Audit


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
    def get_absolute_url(self):
        return reverse('taskupdate', kwargs={'pk': self.pk})


class Aircraft(AVSBaseLookupModel):
    def get_absolute_url(self):
        return reverse('aircraftupdate', kwargs={'pk': self.pk})


class Pilot(ActiveModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('pilotupdate', kwargs={'pk': self.pk})


class AircraftFlightLog(Audit):
    flight_log_number = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    aircraft = models.ForeignKey(Aircraft)
    fire_danger_index = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.flight_log_number)

    def get_absolute_url(self):
        return reverse('aircraftflightlogdetailsadd', kwargs={'id': self.id})


class AircraftFlightLogDetail(Audit):
    datcon = models.DecimalField(max_digits=9, decimal_places=1)
    time_out = models.TimeField(help_text='GMT+8')
    landings = models.IntegerField(default=0)
    fire_number = models.CharField(max_length=50, null=True, blank=True)
    fuel_added = models.IntegerField(default=0)
    task = models.ForeignKey(Task, null=True, blank=True)
    job_number = models.CharField(max_length=30, null=True, blank=True)
    pilot_in_command = models.ForeignKey(
        Pilot, related_name='pilot_in_command')
    pilot_in_command_under_supervision = models.ForeignKey(
        Pilot, null=True, blank=True)
    aircraft_flight_log = models.ForeignKey(AircraftFlightLog)

    def __unicode__(self):
        return unicode(self.id)


class DutyTime(Audit):
    date = models.DateField()
    pilot = models.ForeignKey(Pilot)
    datetime_on_first = models.TimeField(null=True, blank=True)
    datetime_off_first = models.TimeField(null=True, blank=True)
    travel_km = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.remarks)

    def get_absolute_url(self):
        return reverse('dutytimeaddset', kwargs={'id': self.id})
