from django.conf.urls import patterns, url

urlpatterns = patterns('bookmarks.staffviews',
    url(r'^/?$'                     ,'bookmarks_home'            ,name="staff_bookmark_home"),
    url(r'^ajax-listBookmark/$'     ,'ajax_list_bookmark'        ,name="staff_bookmark_ajax_list_bookmarks"),
    url(r'^add/$'                   ,'bookmarks_add'             ,name="staff_bookmark_add"),
    url(r'^ajax-action/?$'          ,'ajax_bookmark_action'      ,name='staff_bookmark_ajax_action'),
    url(r'^ajax-bookmarkState/$'    ,'ajax_bookmark_state'       ,name="staff_bookmark_ajax_state"),
    url(r'^changestatus/$'          ,'bookmark_change_status'    ,name='staff_bookmark_change_status'),
    url(r'^edit/(?P<id>\d+)/$'      ,'bookmark_edit'             ,name="staff_bookmark_edit"),
    url(r'^seo/(?P<id>\d+)/$'       ,'seo'                       ,name='staff_bookmark_seo'), 
    url(r'^ajax-fetch-images/$'     ,'bookmark_fetch_images'     ,name='staff_bookmark_fetch_images'),
    url(r'^ajax-edit-fetch-images/$','bookmark_edit_fetch_images',name='staff_bookmark_edit_fetch_images'),
    url(r'^preview/$'               ,'bookmark_preview'          ,name='staff_bookmark_preview'),
   
)