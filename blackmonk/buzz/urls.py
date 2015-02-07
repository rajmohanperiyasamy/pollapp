from django.conf.urls import *

urlpatterns = patterns('buzz.views',
    url(r'^/?$', 'buzz_home', name="buzz_home"),
    url(r'^(?P<category>[-\w]+)\/?$', 'retrieve_buzz'  ,name='buzz_retrieve_buzz'),
    
    #Ajax
    url(r'^ajax/home/?$', 'ajax_retrieve_search'  ,name='ajax_retrieve_buzz_search'),
    url(r'^ajax/(?P<category>[-\w]+)\/?$', 'ajax_retrieve_buzz'  ,name='ajax_retrieve_buzz')
    
)