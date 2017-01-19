from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', logout, name='logout', kwargs={'template_name': 'logged_out.html'}),
    url(r'^confluence', RedirectView.as_view(url='https://confluence.dec.wa.gov.au/display/AVS'), name='help_page'),
    url(r'^avs/', include('avs.urls')),
    url(r'^$', RedirectView.as_view(url='/avs'), name='site_home'),
]
