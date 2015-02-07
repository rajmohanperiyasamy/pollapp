from django.conf.urls import *

urlpatterns = patterns('locality.views',
            url(r'^getxmllocation/?$', 'getXmlLocation', name='getXmlLocation'),
            url(r'^letlocalitypin/?$', 'auto_suggest_pin', name='letlocalitypin'),
             url(r'^suggest-pin/?$', 'suggest_pin', name='auto_suggest_pin'),
            
)