from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = patterns('',  
   url(r'^$',TemplateView.as_view(template_name='fbconnect/test.html')),
   url(r'^authenticate/?$','fbconnect.views.authenticate', name='fbconnect_login1'),
   url(r'^xd_receiver/$',TemplateView.as_view(template_name='fbconnect/xd_receiver.htm')),
   url(r'^complete/?$','fbconnect.views.associate_fbaccount', name='fbconnect_associate_fbaccount'),
   url(r'^register/?$','fbconnect.views.register', name='fbconnect_register'),
)
