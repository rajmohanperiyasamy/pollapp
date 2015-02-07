from django.conf.urls import *
from payments.googlecheckout.views import *
urlpatterns = patterns('',
           (r'^gc-notify-handler/$', gc_notify_handler),)