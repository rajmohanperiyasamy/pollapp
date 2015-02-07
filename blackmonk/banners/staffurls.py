from django.conf.urls import patterns, url
urlpatterns = patterns('banners.staffviews',
    
    #Banner Management 
    url(r'^/?$', 'manage_banners', name='staff_banners_manage_banners'),
    url(r'^ajax-list-banners/?$','ajax_list_banners',name='staff_banners_ajax_list_banners'), 
    url(r'^ajax-banner-actions/?$','ajax_banner_actions',name='staff_banners_ajax_banner_actions'),
    url(r'^ajax-banner-state/?$', 'ajax_banner_state',name="staff_banners_ajax_banner_state"),
    url(r'^ajax-change-banner-status/?$', 'ajax_change_banner_status',name="staff_banners_ajax_change_banner_status"),
    
    url(r'^addbanner/$', 'add_banner', name='staff_banners_add_banner'),
    url(r'^preview/$', 'preview_banner', name='staff_banners_preview_banner'),
    url(r'^ajax-load-banner-categories/$', 'ajax_load_banner_categories', name='staff_banners_ajax_load_banner_categories'),
    url(r'^ajax-load-banner-zones/$', 'ajax_load_banner_zones', name='staff_banners_ajax_load_banner_zones'),
    url(r'^ajax-load-banner-payment/$', 'ajax_load_banner_payment', name='staff_banners_ajax_load_banner_payment'),
    url(r'^ajax-delete-banner-image/$', 'ajax_delete_banner_image', name='staff_banners_ajax_delete_banner_image'),
    
    url(r'^traffic-reports/$', 'banner_traffic_reports', name='staff_banners_banner_traffic_reports'),
    url(r'^banner-image-preview/$', 'banner_image_preview', name='staff_banners_banner_image_preview'),
    
    url(r'^hero-banners/?$', 'manage_herobanners', name='staff_banners_manage_hero_banners'),
    url(r'^ajax-change-herobanner-status/?$', 'ajax_change_herobanner_status',name="staff_change_herobanner_status"),
    url(r'^addherobanner/$', 'add_hero_banner', name='staff_banners_add_hero_banner'),
    url(r'^ajax-herobanner-delete/?$','ajax_herobanner_delete',name='staff_herobanners_ajax_banner_delete'),
    url(r'^ajax-delete-herobanner-image/$', 'ajax_delete_herobanner_image', name='staff_ajax_delete_herobanner_image'),
    
)
