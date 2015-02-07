from django.conf.urls import patterns, url

urlpatterns = patterns('events.adminviews',
    url(r'^/?$', 'event_settings', name='admin_portal_event'),
    url(r'^settings/?$', 'event_settings', name='admin_portal_event_approval'),
    
    url(r'^category/?$', 'event_category', name='admin_portal_event_category'),
    url(r'^updatecategory/?$', 'event_category_update', name='admin_portal_event_category_update'),
    url(r'^deletecategory/?$', 'event_category_delete', name='admin_portal_event_category_delete'),
    url(r'^seocategoryupdate/?$', 'event_seo_category_update', name='admin_portal_event_seo_category_update'),
   
    url(r'^pricing/$', 'event_price', name='admin_portal_event_price'),
    
)