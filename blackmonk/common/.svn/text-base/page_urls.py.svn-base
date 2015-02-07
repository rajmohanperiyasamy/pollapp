from django.conf.urls import *
urlpatterns = patterns('common.pageviews',
    #PAGE CONFIGURATION 
    url(r'^/?$', 'custom_page', name='admin_custom_page'),
    url(r'^(?P<id>\d+)/$', 'edit_resources', name="edit_resources"),
    url(r'^ajax-image-upload/?$', 'resources_image_upload', name="resources_image_upload"),
    url(r'^status/?$', 'custom_page_status', name='admin_custom_page_status'),
    url(r'^delete/?$', 'custom_page_delete', name='admin_custom_page_delete'),
    
    # OLD URL
    #url(r'^/?$', 'custom_page', name='admin_page'),
    #url(r'^(?P<id>\d+)/?$', 'page', name='admin_page_view'),
    #url(r'^update/?$', 'custom_page_update', name='admin_custom_page_add'),
    #url(r'^update/(?P<id>\d+)/?$', 'custom_page_update', name='admin_custom_page_view'),
)