from django.conf.urls import *
from mobapp.views import v1_api,near_by_locations_events,business_list,near_by_locations_attractions,gloabal_nearby,attraction_list

urlpatterns = patterns('',
                       
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/v1/nearbyevents/?$', near_by_locations_events),
    url(r'^api/v1/nearbyattractions/?$', near_by_locations_attractions),
    url(r'^api/v1/businesslist/?$', business_list),
    url(r'^api/v1/attractionlist/?$', attraction_list),
    url(r'^api/v1/gloabal_nearby/?$', gloabal_nearby),
    
)
