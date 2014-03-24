from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'', include('gmapi.urls.media')), # Use for debugging only.
    (r'^$', 'mapsplay.views.index'),
)