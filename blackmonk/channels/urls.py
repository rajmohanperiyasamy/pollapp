from django.conf.urls import patterns, url

urlpatterns = patterns('channels.views',
    url(r'^/?$', 'channels_home', name='channels_home'),
    #url(r'^catageoy-business-ajax/(?P<id>\d+)/$', 'latest_business_ajax', name="latest_business_ajax"),
    url(r'^catageoy-business-ajax/?$', 'latest_business_ajax', name='latest_business_ajax'),
    url(r'^get-events-by-date/$', 'ajax_get_channel_events_by_date',name='channel_events_ajax_get_events_by_date'),#ajax_get_events_by_date

    
    
)