from django.conf.urls import *

urlpatterns = patterns('',
    #API HOTEl CONFIGURATION 
    url(r'^/?$', 'common.apiviews.api_overviews', name='admin_api_overviews'),
    #API WEATHER CONFIGURATION
    url(r'^weather/?$', 'common.apiviews.weather_configuration', name='admin_api_weather_configuration'),
    url(r'^Weather/ajax-update-settings/?$', 'common.apiviews.update_weather_api_settings', name='admin_api_update_weather_api_settings'),
    
    url(r'^places-to-see/?$', 'common.adminviews.manage_things_to_do', name='admin_config_manage_things_to_do'),
    url(r'^golf/?$', 'common.adminviews.manage_golf', name='admin_config_manage_golf'),
    url(r'^validate-url-api/?$', 'common.adminviews.api_check_url_exist', name='admin_api_check_url_exist'),
    #
    
    url(r'^hotels/', include('hotels.adminurls')),#Buzz
    url(r'^florist/', include('flowers.adminurls')),#Buzz
    url(r'^buzz/', include('buzz.admin_urls')),#Buzz
   
)