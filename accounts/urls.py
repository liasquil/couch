from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

import views


urlpatterns= patterns('',
    
    # although in the accounts-app, these shall be top-level pages.
    # define those url names in the root url conf!
    url(r'login/', RedirectView.as_view(url=reverse_lazy('login')), name="login"),
    url(r'logout/', RedirectView.as_view(url=reverse_lazy('logout')), name="logout"),
    url(r'signup/', RedirectView.as_view(url=reverse_lazy('signup')), name="signup"),
    
    # actual 'accounts'-scope
    url(r'hello/', 'accounts.views.hello', name="hello"),
    url(r'edit-account/$', 'accounts.views.edit_account', name="edit_account"),
    url(r'edit-account/entry:(?P<entry>[a-z]+)/$', 'accounts.views.edit_account', name="edit_account_handler"),
    url(r'edit-profile/$', 'accounts.views.edit_profile', name="edit_profile"),
    url(r'add-language-skill/$', 'accounts.views.add_language_skill', name="add_language_skill"),
    url(r'discard-language-skill/(?P<skill_id>\d+)/$', 'accounts.views.discard_language_skill', name="discard_language_skill"),
    url(r'(?P<user_id>\d+)/profile/$', 'accounts.views.view_profile', name="view_profile"),
    url(r'forgot-password/', 'accounts.views.forgot_password', name='forgot_password'),
    url(r'token-sent/', 'accounts.views.token_sent', name='token_sent'),
    
    url(r'reset-password/(?P<token_value>[a-f0-9]{64})/$', 
        'accounts.views.reset_password', 
        name='reset_password'),
    
    url(r'verify-email/(?P<user_id>\d+)/(?P<verification_code>[a-f0-9]{64})/$', 
        'accounts.views.verify_email', 
        name='verify_email'),
)