from django.conf.urls import *

urlpatterns = patterns('bookmarks.userviews',
                       
    url(r'^/?$'                     , 'dash_board'          , name="bookmark_dash_board"),  
     
    url(r'^ajax-listBookmarks/$'    , 'ajax_dash_board'     , name="bookmark_ajax_dash_board"),
    
    url(r'^add/$'                   , 'add_bookmark'        , name="bookmark_add_bookmark"),
    url(r'^edit/(?P<id>\d+)/$'      , 'edit_bookmark'       , name="bookmark_edit_bookmark"),
    url(r'^ajax-fetch-images/$'     , 'bookmark_fetch_images'     ,name='user_bookmark_fetch_images'),
    url(r'^seo/(?P<id>\d+)/$'       , 'seo'                 , name='bookmark_update_seo'),   
    url(r'^preview/$'               ,'bookmark_preview'          ,name='user_bookmark_preview'),
    url(r'^ajax-action/?$'          , 'ajax_bookmark_action', name='bookmark_ajax_action'), 
    url(r'^ajax-bookmarkState/$'    , 'ajax_bookmark_state' , name="bookmark_ajax_state"),
    url(r'^ajax-edit-fetch-images/$', 'bookmark_edit_fetch_images',name='user_bookmark_edit_fetch_images'),
    url(r'^changestatus/$'          , 'change_status'       , name='bookmark_change_status'),               
)                 