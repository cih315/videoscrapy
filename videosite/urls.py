from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'video.views.home', name='home'),
    # url(r'^videosite/', include('videosite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"])+'/../bootstrap/css'}),

    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"])+'/../bootstrap/img'}),

    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':os.path.dirname(globals()["__file__"]) + '/../bootstrap/js'}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
