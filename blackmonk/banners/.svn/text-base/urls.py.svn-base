from django.conf.urls import patterns, url

urlpatterns = patterns('banners.views',
    #url(r'^/?$', 'gallery_home', name='gallery_home'),
    url(r'^ajax-get-banner/$', 'get_banner_ads', name='banners_get_banner_ads'),
    url(r'^ajax-get-top-banner/$', 'get_banner_ads_top', name='banners_get_banner_ads_top'),
    url(r'^ajax-get-bottom-banner/$', 'get_banner_ads_bottom', name='banners_get_banner_ads_bottom'),
    url(r'^ajax-update-views/$', 'update_banner_views', name='banners_update_banner_views'),
    url(r'^ajax-update-clicks/$', 'update_banner_clicks', name='banners_update_banner_clicks'),
)     