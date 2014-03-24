from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^new/$', 'couches.views.new_couch', name='new_couch'),
    url(r'^request/(?P<couch_id>\d+)/$', 'couches.views.request_couch', name='request_couch'),
    url(r'^request-inbox/$', 'couches.views.request_inbox', name='request_inbox'),
    url(r'^request-outbox/$', 'couches.views.request_outbox', name='request_outbox'),
    url(r'^accept-request/(?P<couch_request_id>\d+)/$', 'couches.views.accept_request', name="accept_request"),
    url(r'^decline-request/(?P<couch_request_id>\d+)/$', 'couches.views.decline_request', name="decline_request"),
    url(r'^(?P<pk>\d+)/$', views.CouchDetailView.as_view(), name='couch_detail'),
    url(r'^search', 'couches.views.search_couch_map', name='search_couch'),
)
 
