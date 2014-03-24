from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns= patterns('',
    
    # although in the accounts-app, these shall be top-level pages.
    # define those url names in the root url conf!
    url(r'new/', 'privatemsg.views.new_message', name="new"),
    url(r'reply-to/(?P<preceding_message_id>\d+)/$', 'privatemsg.views.new_message', name='reply_sender'),
    url(r'reply-to-all/(?P<preceding_message_id>\d+)/$', 'privatemsg.views.new_message', {'answer_all':True}, name='reply_all'),
    url(r'inbox/', 'privatemsg.views.inbox', name="inbox"),
    url(r'outbox/', 'privatemsg.views.outbox', name="outbox"),
    url(r'delete/(?P<message_id>\d+)$', 'privatemsg.views.delete', name="delete"),
)