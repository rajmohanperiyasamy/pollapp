from django.conf.urls import patterns, url

urlpatterns = patterns('videos.adminviews',
    url(r'^/?$', 'videos_settings', name='admin_portal_videos'),
    url(r'^settings/?$', 'videos_settings', name='admin_portal_videos_approval'),
    
    url(r'^category/?$', 'videos_category', name='admin_portal_videos_category'),
    url(r'^updatecategory/?$', 'videos_category_update', name='admin_portal_videos_category_update'),
    url(r'^deletecategory/?$', 'videos_category_delete', name='admin_portal_videos_category_delete'),
    url(r'^seocategoryupdate/?$', 'videos_seo_category_update', name='admin_portal_videos_seo_category_update'),
    
)