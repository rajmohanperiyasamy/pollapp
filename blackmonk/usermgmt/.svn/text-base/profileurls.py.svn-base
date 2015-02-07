from django.conf.urls import patterns, url

urlpatterns = patterns('usermgmt.profileviews',
    url(r'^/?$', 'user_public_profile', name='public_profile'),
    url(r'^(?P<username>[-\w]+)\/?$', 'user_profile', name='user_profile'),
    url(r'^(?P<username>[-\w]+)\/(?P<view>[-\w]+)\/$','user_profile',name="profile_module_deatils"),
    url(r'^ajax_contribution/(?P<username>[-\w]+)\/getcount/$', 'ajax_contribution', name='ajax_contribution'), 
#     url(r'^ajax/(?P<username>[-\w]+)\/(?P<view>[-\w]+)\/$','ajax_profile_module_deatils',name="ajax_profile_module_deatils"), 
    url(r'^ajax/(?P<username>[-\w]+)\/details/$','ajax_profile_module_deatils',name="ajax_profile_module_deatils"), 
)
