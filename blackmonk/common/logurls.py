from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import *

urlpatterns = patterns('common.logviews',
                       
    url(r'^/?$', 'log', name='common_log'),
    url(r'^delete/$', 'log_delete', name='common_log_delete'),
    )
    