from django.conf.urls import *

urlpatterns = patterns('events.views',
                       
          
        url(r'^/?$', 'venue_list', name='events_venue_list'),
        url(r'^type/(?P<cat>((\w+|-)*))\/?$', 'search_venue_list', name='events_search_venue_list_event'),
        url(r'^(?P<venslug>[-\w]+)/$', 'view_venue', name="events_view_venue_event"),
)
                         