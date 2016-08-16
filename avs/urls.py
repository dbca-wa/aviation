#from django.conf.urls.defaults import * depracated
from django.conf.urls import *
from avs.views import *
from avs.migrate import *
from django.conf import settings

urlpatterns = patterns('',      
    # Pilots
    url(r'^pilot/list$', pilotlist, name='pilotlist',),
    url(r'^pilot/list-saved$', pilotlist, name='pilotlist_saved',  kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^pilot/add/$', pilotadd, name='pilotadd'),    
    url(r'^pilot/(?P<pk>\d+)/update$',PilotUpdate.as_view(), name='pilotupdate',),
    # Aircraft
    url(r'^aircraft/list$', aircraftlist, name='aircraftlist',),
    url(r'^aircraft/list-saved$', aircraftlist, name='aircraftlist_saved',  kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^aircraft/add/$', aircraftadd, name='aircraftadd'),
    url(r'^aircraft/(?P<pk>\d+)/update$',AircraftUpdate.as_view(), name='aircraftupdate',),
    # Task
    url(r'^task/list$', tasklist, name='tasklist'),
    url(r'^task/list-saved$', tasklist, name='tasklist_saved',  kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^task/add/$', taskadd, name='taskadd'),
    url(r'^task/(?P<pk>\d+)/update$', TaskUpdate.as_view(), name='taskupdate',),
    # Aircraft Flight Log
    url(r'^aircraftflightlog/list$', aircraftflightloglist, name='aircraftflightlogslist'),
    url(r'^aircraftflightlog/listdetailed$', aircraftflightloglistdetailed, name='aircraftflightloglistdetailed'),
    url(r'^aircraftflightlog/list-saved$', aircraftflightloglist, name='aircraftflightlogslist_saved',  kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^aircraftflightlog/add/$', aircraftflightlogadd, name='aircraftflightlogadd'),
    # Aircraft Flight Log Details
    url(r'^aircraftflightlogdetails/(?P<id>\d+)/add/$', aircraftflightlogdetailsadd, name='aircraftflightlogdetailsadd'),
    url(r'^aircraftflightlogdetails-saved/(?P<id>\d+)/add/$', aircraftflightlogdetailsadd, name='aircraftflightlog_saved', kwargs = {'state':'Saved','state_type':'OK'}),
    # Duty Time    
    url(r'^dutytime/add/$', dutytimeadd, name='dutytimeadd'),    
    url(r'^dutytime/(?P<id>\d+)/add/$', dutytimeaddset, name='dutytimeaddset'),
    url(r'^dutytime-saved/(?P<id>\d+)/add/$', dutytimeaddset, name='dutytimeaddset_saved', kwargs = {'state':'Saved','state_type':'OK'}),
    url(r'^dutytime/(?P<id>\d+)/hours/$', dutytimehours, name='dutytimehours'),
	# Migrate
	url(r'^migrate$', migrate, name='migrate'),
    # Summary Reports	
    # Command
    url(r'^report/commandpilotsummary$', commandpilotsummary, name='commandpilotsummary'),    
    # Training
    url(r'^report/trainingpilotsummary$', trainingpilotsummary, name='trainingpilotsummary'),    
    # Aircraft
    url(r'^report/aircraftsummary$', aircraftsummary, name='aircraftsummary'),    
    # Flight
    url(r'^report/flightsummary$', flightsummary, name='flightsummary'),    
    # Other
    url(r'^report/timesummary$', timesummary, name='timesummary'),    
    url(r'^report/firesummary$', firesummary, name='firesummary'),
)

#urlpatterns += patterns('django.views.generic.simple',
urlpatterns += patterns('django.views.generic',  
    # Index
    #url(r'^index$', 'direct_to_template', {'template': 'index.html','extra_context':{'pagetitle':'Home'}}, name='index'), Depracated


   url(r'^index$', ExtraContextTemplateView.as_view(template_name= 'index.html',extra_context={'pagetitle':'Home'}), name='index'),
	
)

urlpatterns += patterns('django.views.static',
  
    # Media
    #(r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
)

