from django.conf.urls import *
urlpatterns = patterns('common.utilviews',
    url(r'^upload-cover-photo/?$', 'cover_photo', name='common_upload_cover_photo'),
    url(r'^delete-cover-photo/(?P<pk>\d+)/$', 'delete_cover_photo', name='common_delete_cover_photo'),
    url(r'^update-cover-photo/(?P<pk>\d+)/$', 'ajax_crop_and_save', name='common_update_cover_photo'),
    # OLD URL
    #url(r'^(?P<id>\d+)/?$', 'page', name='admin_page_view'),
)