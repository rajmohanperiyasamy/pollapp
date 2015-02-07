from django.conf.urls import *

urlpatterns = patterns('attraction.staffviews',
    url(r'^/?$', 'manage_attraction',name="staff_manage_attraction"),
    url(r'^ajax/?$','ajax_list_attraction',name='ajax_list_attraction'), 
    url(r'^ajax-action/?$','ajax_attraction_action',name='ajax_attraction_action'),
    url(r'^ajax-state/?$', 'ajax_attraction_state',name="ajax_attraction_state"),
    url(r'^seo/(?P<id>\d+)/?$', 'seo_attraction',name="staff_seo_attraction"),
    url(r'^change-status/?$', 'change_status_attraction',name="staff_change_status_attraction"),
    #ADD EDIT
    url(r'^add/?$', 'add_attraction',name="staff_add_attraction"),
    url(r'^update/(?P<id>\d+)/?$', 'edit_attraction',name="staff_edit_attraction"),
    url(r'^preview/(?P<id>\d+)/?$', 'preview_attraction',name="staff_preview_attraction"),
    url(r'^autosuggesttag/?$', 'auto_suggest_tag',name="staff_attraction_auto_suggest_tag"),
    
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='staff_attraction_ajax_upload_photos'),
    url(r'^ajaxuploadphotos-preview/$', 'ajax_upload_photos_preview' ,name='staff_attraction_ajax_upload_photos_preview'),
    url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='staff_attraction_ajax_delete_photos'),
    url(r'^photos/(?P<pk>\d+)$', 'attraction_photos' ,name='staff_photos_attraction'),
    url(r'^photos-status/$', 'change_photo_status_attraction' ,name='staff_change_photo_status_attraction'),
    
    #Videos
    url(r'^videos/$', 'attraction_videos', name='staff_attraction_videos'),
    url(r'^addvideos/$', 'attraction_add_videos', name='staff_attraction_add_videos'),
    url(r'^deletevideos/$', 'attraction_delete_videos', name='staff_attraction_delete_videos'),
    
    url(r'^display_address/$', 'display_address' ,name='staff_attraction_display_address'),
)