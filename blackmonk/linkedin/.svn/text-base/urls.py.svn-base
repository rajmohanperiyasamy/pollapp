from django.conf.urls import patterns, include, url
from linkedin.views import oauth_login,oauth_authenticated

urlpatterns = patterns('',
    url(r'^login/?$', oauth_login, name='linkedin_login'),
    url(r'^login/authenticated/?$', oauth_authenticated, name='linkedin_authenticated'),
    url(r'^complete/?$','linkedin.views.complete', name='linkedin_complete'),
)
