from django.conf.urls import *

urlpatterns = patterns('restaurants.staffviews',
    
    url(r'^/?$', 'manage_restaurant', name="staff_restaurant_home"),
    url(r'^ajax/$','ajax_list_restaurant',name='staff_ajax_list_restaurant'),
    url(r'^ajax-action/?$','ajax_restaurant_action',name='staff_ajax_restaurant_action'),
    url(r'^listingtype/$', 'restaurant_listing_type',name='staff_restaurant_listing_type'),
    url(r'^ajax-state/?$', 'ajax_restaurant_state',name="staff_ajax_restaurant_state"),
    url(r'^change-status/?$', 'change_status_restaurant',name="staff_change_status_restaurant"),
    
    
    
    url(r'^seo_update/(?P<id>\d+)/?$', 'seo_restaurant',name="staff_seo_restaurant"),  
    
    url(r'^add/$', 'add_restaurant', name='staff_add_restaurant'),
    url(r'^preview/(?P<id>\d+)/?$', 'preview_restaurant',name="staff_preview_restaurant"),
    url(r'^update/(?P<id>\d+)/$', 'update_restaurant', name='staff_update_restaurant'),
    
    
    url(r'^ajaxuploadlogo/$', 'ajax_upload_logo' ,name='restaurant_ajax_upload_logo'),
    url(r'^deletelogo/(?P<pk>\d+)/$', 'restaurant_delete_logo', name='restaurant_delete_logo'),
    url(r'^auto-suggest-tags/$', 'auto_suggest_tag', name='restaurant_auto_suggest_tag'),
    

    url(r'^menu/(?P<id>\d+)/?$', 'restaurant_menu',name="staff_restaurant_menu"),
    url(r'^menu-add/(?P<id>\d+)/?$', 'restaurant_add_menu',name="staff_restaurant_menu_add"),
    url(r'^menu-load/?$', 'restaurant_menu_load_html',name="staff_restaurant_menu_load_html"),
    url(r'^menu-delete/?$', 'restaurant_delete_menu',name="staff_restaurant_menu_delete"),
    
    
    url(r'^image/(?P<id>\d+)/?$', 'restaurant_images', name='staff_restaurant_image'),
    url(r'^ajaximageupload/(?P<id>\d+)/?$', 'ajax_upload_image', name="staff_restaurant_ajax_upload_photos"),
    url(r'^ajaxdeleteimage/(?P<pk>\d+)$', 'restaurant_delete_images' ,name='staff_restaurant_ajax_delete_image'),
    url(r'^ajaxupdatephotocaption/(?P<pk>\d+)$', 'ajax_update_photo_caption' ,name='staff_restaurant_ajax_update_photo_caption'),

    
    url(r'^videos/$', 'restaurant_videos', name='staff_restaurant_videos'),
    url(r'^addvideos/$', 'restaurant_ajax_add_videos', name='staff_restaurant_ajax_add_videos'),
    url(r'^deletevideos/$', 'restaurant_ajax_delete_videos', name='staff_restaurant_ajax_delete_videos'),
)