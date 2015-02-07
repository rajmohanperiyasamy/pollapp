from django.conf.urls import patterns, url

urlpatterns = patterns('community.adminviews',
    url(r'^/?$', 'community_settings', name='admin_portal_advice'),
    url(r'^settings/?$', 'community_settings', name='admin_portal_advice_approval'),
    
    url(r'^category/?$', 'advice_category', name='admin_portal_advice_category'),
    url(r'^updatecategory/?$', 'advice_category_update', name='admin_portal_advice_category_update'),
    url(r'^deletecategory/?$', 'advice_category_delete', name='admin_portal_advice_category_delete'),
    url(r'^seocategoryupdate/?$', 'advice_seo_category_update', name='admin_portal_advice_seo_category_update'),
    
)