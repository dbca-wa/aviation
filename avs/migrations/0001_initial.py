# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('effective_from', models.DateTimeField(default=datetime.datetime(2017, 1, 6, 14, 26, 38, 786174))),
                ('effective_to', models.DateTimeField(null=True, blank=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('creator', models.ForeignKey(related_name='avs_aircraft_created', editable=False, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(related_name='avs_aircraft_modified', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AircraftFlightLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('flight_log_number', models.CharField(unique=True, max_length=20)),
                ('date', models.DateField()),
                ('fire_danger_index', models.IntegerField(null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('aircraft', models.ForeignKey(to='avs.Aircraft')),
                ('creator', models.ForeignKey(related_name='avs_aircraftflightlog_created', editable=False, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(related_name='avs_aircraftflightlog_modified', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AircraftFlightLogDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('datcon', models.DecimalField(max_digits=9, decimal_places=1)),
                ('time_out', models.TimeField(help_text='GMT+8')),
                ('landings', models.IntegerField(default=0)),
                ('fire_number', models.CharField(max_length=50, null=True, blank=True)),
                ('fuel_added', models.IntegerField(default=0)),
                ('job_number', models.CharField(max_length=30, null=True, blank=True)),
                ('aircraft_flight_log', models.ForeignKey(to='avs.AircraftFlightLog')),
                ('creator', models.ForeignKey(related_name='avs_aircraftflightlogdetail_created', editable=False, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(related_name='avs_aircraftflightlogdetail_modified', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DutyTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('datetime_on_first', models.TimeField(null=True, blank=True)),
                ('datetime_off_first', models.TimeField(null=True, blank=True)),
                ('travel_km', models.IntegerField(null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('creator', models.ForeignKey(related_name='avs_dutytime_created', editable=False, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(related_name='avs_dutytime_modified', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pilot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('effective_from', models.DateTimeField(default=datetime.datetime(2017, 1, 6, 14, 26, 38, 786174))),
                ('effective_to', models.DateTimeField(null=True, blank=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('code', models.CharField(unique=True, max_length=3)),
                ('creator', models.ForeignKey(related_name='avs_pilot_created', editable=False, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(related_name='avs_pilot_modified', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('effective_from', models.DateTimeField(default=datetime.datetime(2017, 1, 6, 14, 26, 38, 786174))),
                ('effective_to', models.DateTimeField(null=True, blank=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('creator', models.ForeignKey(related_name='avs_task_created', editable=False, to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(related_name='avs_task_modified', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='dutytime',
            name='pilot',
            field=models.ForeignKey(to='avs.Pilot'),
        ),
        migrations.AddField(
            model_name='aircraftflightlogdetail',
            name='pilot_in_command',
            field=models.ForeignKey(related_name='pilot_in_command', to='avs.Pilot'),
        ),
        migrations.AddField(
            model_name='aircraftflightlogdetail',
            name='pilot_in_command_under_supervision',
            field=models.ForeignKey(blank=True, to='avs.Pilot', null=True),
        ),
        migrations.AddField(
            model_name='aircraftflightlogdetail',
            name='task',
            field=models.ForeignKey(blank=True, to='avs.Task', null=True),
        ),
    ]
