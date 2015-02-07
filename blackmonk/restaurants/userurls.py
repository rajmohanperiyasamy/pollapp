from django.conf.urls import patterns, url

urlpatterns = patterns('restaurants.userviews', 
                       
    url(r'^/?$', 'manage_restaurant', name='user_manage_restaurant'),
    url(r'^ajax/?$','ajax_list_restaurant',name='user_ajax_list_restaurant'),
    url(r'^add/$', 'add_restaurant', name='user_add_restaurant'),   
    url(r'^ajax-action/?$','ajax_restaurant_action',name='user_ajax_restaurant_action'),
    url(r'^ajax-state/?$', 'ajax_restaurant_state',name="user_ajax_restaurant_state"),
    
    url(r'^preview/(?P<id>\d+)/?$', 'preview_restaurant',name="user_preview_restaurant"),
    url(r'^update/(?P<id>\d+)/$', 'update_restaurant', name='user_update_restaurant'),
    url(r'^seo/(?P<id>\d+)/?$', 'seo_restaurant',name="user_seo_restaurant"),
    url(r'^upgrade-listing/(?P<id>\d+)/$', 'restaurant_upgrade_listing_type',name='user_restaurant_upgrade_listing_type'),
    
     url(r'^menu/(?P<id>\d+)/?$', 'restaurant_menu',name="user_restaurant_menu"),
     url(r'^image/(?P<id>\d+)/?$', 'restaurant_image', name='user_restaurant_image'),
     url(r'^videos/$', 'restaurant_video', name='user_restaurant_video'),
                        
                       
                       
)