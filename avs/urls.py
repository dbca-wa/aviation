from django.conf.urls import url
from avs import views as avs_views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # Pilots
    url(r'^pilot/list$', avs_views.pilotlist, name='pilotlist',),
    url(r'^pilot/list-saved$', avs_views.pilotlist, name='pilotlist_saved', kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^pilot/add/$', avs_views.pilotadd, name='pilotadd'),
    url(r'^pilot/(?P<pk>\d+)/update$', avs_views.PilotUpdate.as_view(), name='pilotupdate',),
    # Aircraft
    url(r'^aircraft/list$', avs_views.aircraftlist, name='aircraftlist',),
    url(r'^aircraft/list-saved$', avs_views.aircraftlist, name='aircraftlist_saved',  kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^aircraft/add/$', avs_views.aircraftadd, name='aircraftadd'),
    url(r'^aircraft/(?P<pk>\d+)/update$', avs_views.AircraftUpdate.as_view(), name='aircraftupdate',),
    # Task
    url(r'^task/list$', avs_views.tasklist, name='tasklist'),
    url(r'^task/list-saved$', avs_views.tasklist, name='tasklist_saved', kwargs={'state':'Saved','state_type':'OK'}),
    url(r'^task/add/$', avs_views.taskadd, name='taskadd'),
    url(r'^task/(?P<pk>\d+)/update$', avs_views.TaskUpdate.as_view(), name='taskupdate',),
    # Aircraft Flight Log
    url(r'^aircraftflightlog/list$', avs_views.aircraftflightloglist, name='aircraftflightlogslist'),
    url(r'^aircraftflightlog/listdetailed$', avs_views.aircraftflightloglistdetailed, name='aircraftflightloglistdetailed'),
    url(r'^aircraftflightlog/list-saved$', avs_views.aircraftflightloglist, name='aircraftflightlogslist_saved',  kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^aircraftflightlog/add/$', avs_views.aircraftflightlogadd, name='aircraftflightlogadd'),
    # Aircraft Flight Log Details
    url(r'^aircraftflightlogdetails/(?P<id>\d+)/add/$', avs_views.aircraftflightlogdetailsadd, name='aircraftflightlogdetailsadd'),
    url(r'^aircraftflightlogdetails-saved/(?P<id>\d+)/add/$', avs_views.aircraftflightlogdetailsadd, name='aircraftflightlog_saved', kwargs = {'state':'Saved','state_type':'OK'}),
    # Duty Time
    url(r'^dutytime/add/$', avs_views.dutytimeadd, name='dutytimeadd'),
    url(r'^dutytime/(?P<id>\d+)/add/$', avs_views.dutytimeaddset, name='dutytimeaddset'),
    url(r'^dutytime-saved/(?P<id>\d+)/add/$', avs_views.dutytimeaddset, name='dutytimeaddset_saved', kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^dutytime/(?P<id>\d+)/hours/$', avs_views.dutytimehours, name='dutytimehours'),
    # Summary Reports
    # Command
    url(r'^report/commandpilotsummary$', avs_views.commandpilotsummary, name='commandpilotsummary'),
    # Training
    url(r'^report/trainingpilotsummary$', avs_views.trainingpilotsummary, name='trainingpilotsummary'),
    # Aircraft
    url(r'^report/aircraftsummary$', avs_views.aircraftsummary, name='aircraftsummary'),
    # Flight
    url(r'^report/flightsummary$', avs_views.flightsummary, name='flightsummary'),
    # Other
    url(r'^report/timesummary$', avs_views.timesummary, name='timesummary'),
    url(r'^report/firesummary$', avs_views.firesummary, name='firesummary'),
]
