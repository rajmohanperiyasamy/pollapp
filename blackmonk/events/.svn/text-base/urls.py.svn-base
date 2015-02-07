from django.conf.urls import *

urlpatterns = patterns('events.views',
                       
        
        url(r'^/?$', 'display_events', name='events_home_event'),
        url(r'^(?P<day>[-\w]+)(.shtml)/?$', 'display_events', name='events_display_events'),
        
        url(r'^date/(?P<year>\d{4}),(?P<month>\d+),(?P<day>\d+)\/?$', 'display_cal_events', name='events_display_cal_events'),
        
        url(r'^free-events/$', 'free_events', name='events_free_events'),
        url(r'^(?P<slug>[-\w]+)(.html)/?$', 'event_detail', name='events_display_event'),
        
        url(r'^goevent/', 'go_event', name='events_go_event'), 
        url(r'^ajaxtellafriend/?$','ajax_tell_a_friend', name='events_ajax_tell_a_friend'),
        url(r'^eventsearch/?$', 'search_event', name='events_search_event'),
        url(r'^eventlistretrieve/', 'event_retrieve_list', name='event_retrieve_list'),
        
        url(r'^autosuggest/$', 'auto_suggest', name='events_auto_suggest'),
        url(r'^autosuggesttag/$', 'auto_suggest_tag',name='events_auto_suggest_tag'), 
        url(r'^add_to_fav/?$', 'event_add_to_fav',name="event_add_to_fav"),  
        
        url(r'^ajaxrsvp/$', 'event_event_rsvp',name='events_event_event_rsvp'),#ajax event rsvp   
        url(r'^ajax-get-rsvp-status/$', 'event_get_rsvp_status',name='events_event_get_rsvp_status'),#ajax event rsvp user status
        url(r'^get-events-by-date/$', 'ajax_get_events_by_date',name='events_ajax_get_events_by_date'),#ajax_get_events_by_date
        url(r'^ajax-popular-venue/?$','ajax_popular_venue', name='ajax_popular_venue'),
        url(r'^(?P<slug>[-\w]+)/?$', 'attribute_search', name='events_attribute_search'),
        
)
                         