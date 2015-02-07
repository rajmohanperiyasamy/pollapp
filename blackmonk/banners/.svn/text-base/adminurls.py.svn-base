from django.conf.urls import patterns, url
urlpatterns = patterns('banners.adminviews',
    
    #CONFIGURATION 
    url(r'^/?$', 'mange_banner_zones', name='admin_configuration_mange_banner_zones'),
    url(r'^addbannerzone/?$', 'add_banner_zone', name='admin_configuration_banners_add_zone'),
    url(r'^deletebannerzone/?$', 'delete_banner_zone', name='admin_configuration_banners_delete_banner_zone'),
    url(r'^pricing/?$', 'banner_payment_settings', name='admin_configuration_banners_banner_payment_settings'),
    url(r'^settings/?$', 'banner_settings', name='admin_configuration_banner_settings'),
    
)