from django.conf.urls import patterns, url

urlpatterns = patterns('locality.adminviews',
    url(r'^/?$','locality',name='admin_portal_locality'),

    url(r'^zipcode/?$', 'locality_zipcode', name='admin_portal_locality_zipcode'),
    url(r'^ajaxzipcode/?$', 'locality_zipcode_ajax', name='admin_portal_locality_zipcode_ajax'),
    url(r'^updatezipcode/?$', 'locality_zipcode_update', name='admin_portal_locality_zipcode_update'),
    url(r'^deletezipcode/?$', 'locality_zipcode_delete', name='admin_portal_locality_zipcode_delete'),
    
    url(r'^venuetype/?$', 'locality_venuetype', name='admin_portal_locality_venuetype'),
    url(r'^ajaxvenuetype/?$', 'locality_venuetype_ajax', name='admin_portal_locality_venuetype_ajax'),
    url(r'^updatevenuetype/?$', 'locality_venuetype_update', name='admin_portal_locality_venuetype_update'),
    url(r'^deletevenuetype/?$', 'locality_venuetype_delete', name='admin_portal_locality_venuetype_delete'),
    
    
    url(r'^venue/?$', 'locality_venue', name='admin_portal_locality_venue'),
    url(r'^addvenue/?$', 'locality_venue_update', name='admin_portal_locality_venue_add'),
    url(r'^updatevenue/(?P<id>\d+)/?$', 'locality_venue_update', name='admin_portal_locality_venue_edit'),
    url(r'^deleteevenue/?$', 'locality_venue_delete', name='admin_portal_locality_venue_delete'),
    
    url(r'^seo/?$', 'locality_venue_seo', name='admin_portal_locality_venue_seo'),
    url(r'^seoupdate/?$', 'locality_venue_seo_update', name='admin_portal_locality_venue_seo_update'),
    
    url(r'^auto-suggest-pin/?$', 'locality_auto_suggest_pin', name='admin_locality_auto_suggest_pin'),
    url(r'^upload-photo/?$', 'locality_ajax_upload_photos', name='admin_locality_ajax_upload_photos'),
    url(r'^delete-photo/(?P<pk>\d+)/?$', 'locality_ajax_delete_photos', name='admin_locality_ajax_delete_photos'),
)