from django.conf.urls import patterns, url

urlpatterns = patterns('gallery.adminviews',
    url(r'^/?$', 'gallery_settings', name='admin_portal_gallery'),
    url(r'^settings/?$', 'gallery_settings', name='admin_portal_gallery_approval'),
    
    url(r'^category/?$', 'gallery_category', name='admin_portal_gallery_category'),
    url(r'^updatecategory/?$', 'gallery_category_update', name='admin_portal_gallery_category_update'),
    url(r'^deletecategory/?$', 'gallery_category_delete', name='admin_portal_gallery_category_delete'),
    url(r'^seocategoryupdate/?$', 'gallery_seo_category_update', name='admin_portal_gallery_seo_category_update'),
    
)