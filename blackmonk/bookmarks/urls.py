from django.conf.urls import *

urlpatterns = patterns('bookmarks.views',
    url(r'^/?$'                                 , 'list_bookmarks'          , name="bookmark_list"),
    url(r'^(?P<catslug>[-\w]+)/$'               , 'bookmark_category_list'  , name="bookmark_category_list"),
    url(r'^(?P<slug>[-\w]+)(.html)/?$'          , 'bookmark_details'        , name="bookmark_details"),
    url(r'^ajaxtellafriend/?$'                  , 'ajax_tell_a_friend'      , name='bookmark_ajax_tell_friend'),
    
    url(r'^a/bookmark-search/?$', 'search_bookmark', name='search_bookmark'),
)
