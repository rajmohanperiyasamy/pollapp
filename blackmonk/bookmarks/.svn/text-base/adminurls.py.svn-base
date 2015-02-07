from django.conf.urls import patterns, url

urlpatterns = patterns('bookmarks.adminviews',
    url(r'^/?$'                     , 'bookmarks_settings'                   , name='admin_portal_bookmarks'),
    url(r'^settings/?$'             , 'bookmarks_settings'          , name='admin_portal_bookmarks_approval'),
    #CATEGORY
    url(r'^category/?$'             , 'bookmarks_category'          , name='admin_portal_bookmarks_category'),
    url(r'^updatecategory/?$'       , 'bookmarks_category_update'   , name='admin_portal_bookmarks_category_update'),
    url(r'^deletecategory/?$'       , 'bookmarks_category_delete'   , name='admin_portal_bookmarks_category_delete'),
    
    url(r'^category-update-seo/?$'  , 'bookmarks_seo_category_update',name='admin_portal_bookmarks_seo_category_update'),
   
)