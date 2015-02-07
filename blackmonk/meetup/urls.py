from django.conf.urls import *

urlpatterns = patterns('meetup.views',
                       
    url(r'^home-ajax/?$', 'meetups', name="meetup_home_ajax"),
    url(r'^more-meetups/?$', 'more_meetups', name="meetup_more_meetups"),
    url(r'^/?$', 'index',name="meetup_index"),
    url(r'^(?P<category>[-\w]+)\/?$', 'index', name='meetup_cat_index'),
     
   
)