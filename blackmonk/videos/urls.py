from django.conf.urls import *

urlpatterns = patterns('videos.views',
            url(r'^/?$','home',name='videos_videos_by_category'),
            url(r'^a/setfavorite/','set_favourite',name='videos_home_set_favourite'), 
            url(r'^ajaxtellafriend/?$','ajax_tell_a_friend',name='videos_ajax_tell_a_friend'), 
            url(r'^a/ajaxmostviewed/?$','video_ajax_mostviewed',name='videos_video_ajax_mostviewed'),      
            url(r'^addtofav/?$', 'videos_add_to_fav',name="videos_add_to_fav"), 

            url(r'^brightcov/?$', 'brightcove_videos',name="videos_brightcove_videos"), 
            url(r'^brightcov/(?P<bslug>[-\w]+)\.html/?$','brightcove_video_details', name='brightcove_video_details'),

            url(r'^(?P<slug>[-\w]+)(.html)\/?$','video_details', name='videos_video_details'),
            url(r'^(?P<catslug>[-\w]+)/$','home',name='videos_videos_by_category'),#this view is now using new page
            url(r'^a/videos-search/?$', 'search_videos', name='search_videos'),
            )

