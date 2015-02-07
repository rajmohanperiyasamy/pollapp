from django.conf.urls import *

urlpatterns = patterns('common.seoviews',
    #SEO FORMAT CONFIGURATION 
    url(r'^/?$', 'seo_overview', name='admin_seo_overview'),
    url(r'^update-seo-settings/?$', 'update_seo_settings', name='admin_seo_update_seo_settings'),
    )