from django.conf.urls import patterns, url

urlpatterns = patterns('attraction.adminviews',
    url(r'^/?$', 'attraction_settings', name='admin_portal_attraction'),
    url(r'^settings/?$', 'attraction_settings', name='admin_portal_attraction_settings'),
    
    url(r'^category/?$', 'attraction_category', name='admin_portal_attraction_category'),
    url(r'^updatecategory/?$', 'attraction_category_update', name='admin_portal_attraction_category_update'),
    url(r'^deletecategory/?$', 'attraction_category_delete', name='admin_portal_attraction_category_delete'),
    url(r'^seocategoryupdate/?$', 'attraction_seo_category_update', name='admin_portal_attraction_seo_category_update'),
)