from django.conf.urls import *

urlpatterns = patterns('sweepstakes.views',
    url(r'^/?$', 'home',name="sweepstakes_home"),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/?$', 'detail',name="sweepstakes_detail"),

    url(r'^saveuser/(?P<id>\d+)/?$', 'register_user', name='contest_register_user'),
    url(r'^rules/(?P<id>\d+)/?$', 'contest_rules', name='contest_rules'),
    url(r'^ajaxaddfbpoint/(?P<id>\d+)/?$', 'ajax_add_fbpoint', name='contest_ajax_add_fbpoint'),
    url(r'^ajaxtellafriend/(?P<id>\d+)/?$', 'ajaxtellafriend', name='contest_ajaxtellafriend'),
    
)