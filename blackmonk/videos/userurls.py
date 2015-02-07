from django.conf.urls import *

urlpatterns = patterns('videos.userviews',


                url(r'^/?$', 'user_home_listing',name='user_video_home_listingboard'),
                url(r'^add/?$','add_video', name='user_video_add'),
                
                 
                url(r'^ajaxdisplay/?$','user_ajax_display_video',name='user_video_ajax_display_video'),
                url(r'^ajax-action/?$','user_ajax_video_action',name='user_video_ajax_action'),
                url(r'^youtube-user-video-adding/?$','youtube_ajax_video_adding_user',name='user_video_ajax_adding'),  # after selecting videos from the youtube here we will add category
                
                url(r'^vimeo-video-search/?$','vimeo_ajax_video_search',name='user_video_ajax_vimeo_search'),
                
                url(r'^ajax-video-edit/?$','ajax_user_video_edit',name='user_video_ajax_edit_video'),
                url(r'^edit-selected-video/?$','edit_selected',name='user_video_edit_selected_video'),
                url(r'^save-status-user-video/?$','change_status',name='user_video_change_status'),
                url(r'ajax-user-video-seo/?$','ajax_user_video_seo',name='user_videos_ajax_video_seo'),
                url(r'^(?P<slug>[-\w]+)/?$','video_preview', name='videos_video_preview'),    


)