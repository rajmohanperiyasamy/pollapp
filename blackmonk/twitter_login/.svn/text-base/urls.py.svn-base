from django.conf.urls import patterns, url

from twitter_login.views import Authorize,Return,associate

urlpatterns = patterns ('',
    url(r'^oauth/authorize/$', Authorize.as_view(), name='oauth_authorize'),
    url(r'^oauth/return/$', Return.as_view(), name='oauth_return'),
    url(r'^associate/?$', associate, name='oauth_associate'),
)