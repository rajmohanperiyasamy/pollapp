from django.conf.urls import patterns, url

from openid_login.views import Begin,Callback


urlpatterns = patterns('',
    url(r'^openid/$', Begin.as_view(), name='openid_begin'),
    url(r'^openid/complete/$', Callback.as_view(), name='openid_callback'),
)