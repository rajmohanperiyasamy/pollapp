from django.conf.urls import *
urlpatterns = patterns('channels.staffviews',
    url(r'^/?$', 'manage_channel', name='staff_channel_manage_channel'),
#    url(r'^add/?$', 'channel_add', name='admin_channel_add_cahnnel'),
    url(r'^update/(?P<id>\d+)/$', 'channel_add', name='staff_channel_update_channel'),
    url(r'^ajax-action/?$','ajax_channel_action',name='staff_channel_ajax_action'),
    url(r'^ajax-channelState/$', 'ajax_channel_state', name="staff_channel_ajax_state"),
    url(r'^ajax-listChannels/$', 'ajax_list_channels', name="staff_channel_ajax_list_channels"),
    url(r'^changestatus/$', 'change_status', name='staff_channel_change_status'),
    url(r'^seo/(?P<id>\d+)/$','seo',name='staff_channel_seo'), 
#    url(r'^channel-status/?$', 'channel_status', name='admin_channel_status'),
)