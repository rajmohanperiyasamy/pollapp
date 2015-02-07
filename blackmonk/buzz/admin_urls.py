from django.conf.urls import *

urlpatterns = patterns('buzz.adminviews',
                       
    url(r'^/?$', 'buzz_settings', name="adminportal_buzz_home"),
    url(r'^settings/?$', 'buzz_settings', name='admin_api_twitter_configuration'),
    url(r'^ajax-update-settings/?$', 'update_api_settings', name='admin_api_update_twitterapi_settings'),
    
    url(r'^categories/$', 'buzz_categories' , name="adminportal_buzz_categories"),
    url(r'^updatecategory/?$', 'buzz_category_update', name='adminportal_buzz_category_update'),
    url(r'^deletecategory/?$', 'buzz_category_delete', name='adminportal_buzz_category_delete'),
   
    url(r'^twitterlists/$', 'buzz_twitter_lists' , name="adminportal_buzz_twitter_lists"),
    url(r'^updatelist/?$', 'buzz_lists_update', name='adminportal_buzz_twitter_update'),
    url(r'^deletelist/?$', 'buzz_lists_delete', name='adminportal_buzz_twitter_delete'),
   
    
)
  