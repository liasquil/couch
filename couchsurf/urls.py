from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'couch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^user/', include('accounts.urls', namespace="accounts")),
    url(r'^signup/', 'accounts.views.signup', name='signup'),
    url(r'^login/', 'accounts.views.login_page', name='login'),
    url(r'^logout/', 'accounts.views.logout_page', name='logout'),
    
    url(r'^messages/', include('privatemsg.urls', namespace="privatemsg")),
    url(r'^couches/', include('couches.urls', namespace="couches")),
    
    url(r'^mapsplay/', include('mapsplay.urls', namespace="mapsplay")),
)
