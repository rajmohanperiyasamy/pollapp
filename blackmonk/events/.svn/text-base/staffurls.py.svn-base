from django.conf.urls import *

urlpatterns = patterns('events.staffviews',
    
    url(r'^/?$', 'display_events',name="staff_event_home"),
    
    url(r'^ajax_displayEvents/$', 'ajax_display_events', name='staff_events_ajax_display_events'),
    url(r'^ajax-action/?$','ajax_event_action',name='staff_event_ajax_action'),
    url(r'^ajax_eventsstate/$', 'ajax_event_state', name='events_staff_ajax__state'),
    
    # Add/Edit Event
    url(r'^add/$', 'add_event', name='events_staff_addevent'),
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='staff_events_ajax_upload_photos'),
    url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='staff_events_ajax_delete_photos'),
    url(r'^defaultphotos/$', 'ajax_get_default_photos' ,name='staff_event_ajax_get_default_photos'),
    url(r'^offline-payment/(?P<eid>\d+)/?$', 'event_offline_payment', name="event_offline_payment"),
    
    url(r'^ajaxaddVenue/$', 'ajax_add_venue' ,name='staff_events_ajax_add_venue'),
    url(r'^displayAdrss/$', 'display_address',name='staff_events_display_address'),
    
    url(r'^time-repeat/$', 'time_repeat',name='staff_events_time_repeat'),
    url(r'^listingtype/$', 'event_listing_type',name='staff_events_listing_type'), 
    url(r'^seo/(?P<id>\d+)/$','seo',name='staff_events_seo'), 
    url(r'^changestatus/$', 'change_status', name='staff_events_change_status'),
    
    url(r'^preview/(?P<id>\d+)/?$', 'event_preview',name="staff_events_preview"),
    #IMPORT/EXPORT
    url(r'export-csv/?$','events_export_csv',name="staff_events_export_csv"),
    url(r'import-csv/?$','events_import_csv',name="staff_events_import_csv"),
)
    
