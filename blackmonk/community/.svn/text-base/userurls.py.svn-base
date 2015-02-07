from django.conf.urls import *

urlpatterns = patterns('community.userviews',
    url(r'^/?$', 'manage_advice',name="user_manage_advice"),
    url(r'^ajax/?$','ajax_list_advice',name='ajax_list_advice'), 
    url(r'^ajax-action/?$','ajax_advice_action',name='ajax_advice_action'),
    url(r'^ajax-state/?$', 'ajax_advice_state',name="ajax_advice_state"),
    #ADD EDIT
    #url(r'^add/?$', 'add_advice',name="user_add_advice"),
    url(r'^preview/(?P<id>\d+)/?$', 'preview_advice',name="user_preview_advice"),
    url(r'^autosuggesttag/?$', 'auto_suggest_tag',name="user_advice_auto_suggest_tag"),
)