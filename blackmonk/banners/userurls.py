from django.conf.urls import patterns, url
urlpatterns = patterns('banners.userviews',
    
    #Banner Management 
    url(r'^/?$', 'manage_banners', name='user_banners_manage_banners'),
    url(r'^ajax-list-banners/?$','ajax_list_banners',name='user_banners_ajax_list_banners'), 
    url(r'^ajax-banner-actions/?$','ajax_banner_actions',name='user_banners_ajax_banner_actions'),
    url(r'^ajax-banner-state/?$', 'ajax_banner_state',name="user_banners_ajax_banner_state"),
    url(r'^ajax-change-banner-status/?$', 'ajax_change_banner_status',name="user_banners_ajax_change_banner_status"),
    url(r'^addbanner/$', 'add_banner', name='user_banners_add_banner'),
    url(r'^preview/$', 'preview_banner', name='user_banners_preview_banner'),
    url(r'^ajax-load-banner-payment/$', 'ajax_load_banner_payment', name='user_banners_ajax_load_banner_payment'),
    url(r'^ajax-delete-banner-image/$', 'ajax_delete_banner_image', name='user_banners_ajax_delete_banner_image'),
    url(r'^traffic-reports/$', 'banner_traffic_reports', name='user_banners_banner_traffic_reports'),
    
)
