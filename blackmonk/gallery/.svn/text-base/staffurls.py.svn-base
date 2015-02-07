from django.conf.urls import patterns, url

urlpatterns = patterns('gallery.staffviews',
        url(r'^/?$', 'manage_gallery', name='staff_manage_gallery'),
        url(r'^ajax/?$','ajax_list_gallery',name='ajax_list_gallery'), 
        url(r'^ajax-state/?$','ajax_gallery_state',name='ajax_gallery_state'),
        url(r'^ajax-action/?$','ajax_gallery_action',name='ajax_gallery_action'),
        url(r'^change-status/?$', 'change_status_gallery',name="staff_change_status_gallery"),
        url(r'^seo/(?P<id>\d+)/$', 'seo', name="staff_gallery_seo"),
        
        url(r'^add/$', 'add_gallery', name='staff_add_gallery'),
        url(r'^update/(?P<id>\d+)/$', 'gallery_update', name='staff_gallery_update'),
        url(r'^addphoto/(?P<id>\d+)/$', 'add_gallery_add_photos', name='staff_add_gallery_add_photos'),
        url(r'^addphotodetails/(?P<id>\d+)/$', 'add_gallery_add_photo_details' ,name='staff_add_gallery_add_photo_details'),
        
        url(r'^details/(?P<id>\d+)/$', 'gallery_detail', name="staff_gallery_detail"),
        url(r'^photo-details/(?P<id>\d+)/$', 'gallery_photo_detail', name="staff_gallery_photo_detail"),
        url(r'^photo-delete/$', 'gallery_photo_delete', name="staff_gallery_photo_delete"),
        url(r'^ajaxupdatephotocaption/(?P<pk>\d+)$', 'ajax_update_photo_caption' ,name='gallery_ajax_update_photo_caption'),
        #COMMON FUNCTIONS
        url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='gallery_ajax_upload_photos'),
        url(r'^ajaxdeletephoto/(?P<pk>\d+)$', 'ajax_delete_photo' ,name='gallery_ajax_delete_photo'),
        url(r'^autosuggesttag/$', 'auto_suggest_tag', name='gallery_auto_suggest_tag'),
        url(r'^ajax-set-cover-image/$', 'set_cover_image', name='staff_set_cover_image'),
)