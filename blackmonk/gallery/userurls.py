from django.conf.urls import patterns, url

urlpatterns = patterns('gallery.userviews',
        url(r'^/?$', 'manage_gallery', name='user_manage_gallery'),
        url(r'^ajax/?$','ajax_list_gallery',name='user_ajax_list_gallery'), 
        url(r'^ajax-state/?$','ajax_gallery_state',name='user_ajax_gallery_state'),
        url(r'^ajax-action/?$','ajax_gallery_action',name='user_ajax_gallery_action'),
        url(r'^seo/(?P<id>\d+)/$', 'seo', name="user_gallery_seo"),
        
        url(r'^add/$', 'add_gallery', name='user_add_gallery'),
        url(r'^update/(?P<id>\d+)/$', 'gallery_update', name='user_gallery_update'),
        url(r'^addphoto-flickr/(?P<id>\d+)/$', 'add_gallery_add_flickr_photos', name='user_add_gallery_add_photos'),
        url(r'^add-photo/(?P<id>\d+)/$', 'add_gallery_add_photos', name='user_add_gallery_upload_photos'),
        url(r'^addphotodetails/(?P<id>\d+)/$', 'add_gallery_add_photo_details' ,name='user_add_gallery_add_photo_details'),
        
        url(r'^details/(?P<id>\d+)/$', 'gallery_detail', name="user_gallery_detail"),
        url(r'^photo-details/(?P<id>\d+)/$', 'gallery_photo_detail', name="user_gallery_photo_detail"),
        url(r'^photo-delete/$', 'gallery_photo_delete', name="user_gallery_photo_delete"),
        url(r'^album-submit/$', 'gallery_submit', name="user_gallery_submit"),
        url(r'^autosuggesttag/$', 'auto_suggest_tag', name='gallery_auto_suggest_tag'),
)