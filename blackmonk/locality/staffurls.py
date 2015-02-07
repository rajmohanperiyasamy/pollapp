from django.conf.urls import *

urlpatterns = patterns('locality.staffviews',
    
     ####### Manage Locality ########
     url(r'^/?$', 'manage_location', name='locality_manage_location'),
     url(r'^add/$', 'add_location', name='locality_add_location'),
     url(r'^delete/$', 'delete_location', name='locality_delete_location'),
     url(r'^edit/$', 'edit_location', name='locality_edit_location'),
     url(r'getlocality/', 'get_locality', name='locality_get_locality'),
     
     ####### Manage Zip Code ##########
     url(r'^zip/$', 'manage_zip', name='locality_manage_zip'),
     url(r'^addzip/$', 'add_zip', name='locality_add_zip'),
     url(r'^delete_zip/$','delete_zip', name='locality_delete_zip'),
     
     ######################## COMMON FUNCTION #########################
     url(r'^autosugges_venue/?$', 'common_auto_suggest_venue', name='staff_common_auto_suggest_venue'),
     url(r'^autosugges_zip/?$', 'common_auto_suggest_zip', name='staff_common_auto_suggest_zip'),
     url(r'^addVenue/$', 'common_ajax_add_venue' ,name='staff_common_ajax_add_venue'),
    )