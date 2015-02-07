from django.conf.urls import *

urlpatterns = patterns('events.userviews',
    url(r'^/?$', 'dash_board',name="events_dash_board"), 
    
    url(r'^ajax_displayEvents/$', 'ajax_display_events', name='events_ajax_display_events'),   
    url(r'^ajax-action/?$','ajax_event_action',name='events_ajax_action'),
    url(r'^ajax_eventsstate/$', 'ajax_event_state', name='events_ajax__state'),
    
    url(r'^add/$', 'add_event', name='events_addevent'),
    url(r'^payment/$', 'event_payment', name='events_event_payment'),
    url(r'^choose-listing-type/(?P<id>\d+)/$', 'ajax_event_payment', name='events_ajax_payment'),
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='events_ajax_upload_photos'),
    url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='events_ajax_delete_photos'),
    url(r'^defaultphotos/$', 'ajax_get_default_photos' ,name='events_ajax_get_default_photos'),       
    
    url(r'^time-repeat/$', 'time_repeat',name='events_time_repeat'), 
    url(r'^ajaxaddVenue/$', 'ajax_add_venue' ,name='events_ajax_add_venue'),
    url(r'^seo/(?P<id>\d+)/$','seo',name='events_update_seo'), 
    url(r'^autosuggest/$', 'auto_suggest', name='auto_suggest_venue'),
    url(r'^displayAdrss/$', 'display_address',name='user_events_display_address'),
    url(r'^preview/(?P<id>\d+)/?$', 'event_user_preview',name="user_event_preview"),
)