from django.conf.urls import patterns,url


 
urlpatterns = patterns('videos.staffviews',
         #Video Landing Page
          url(r'^/?$', 'display_video',name='staff_video_home'),
        
         #Video Listing and Filter
         url(r'^displayVideos/?$', 'display_video', name='video_display_video'),
         url(r'^ajax_displayVideo/?$', 'ajax_display_video', name='staff_video_ajax_display_video'),
         url(r'^ajax-action/?$','ajax_video_action',name='staff_video_ajax_action'),
         url(r'^ajax-video-sidebar/?$','ajax_video_state',name='video_staff_ajax__state'),
         
         #Video Adding
         url(r'^vimeo-video-search/?$','vimeo_ajax_video_search',name='staff_video_ajax_vimeo_search'),
         
         url(r'^youtube-video-adding/?$','youtube_ajax_video_adding',name='staff_video_ajax_adding'),  # after selecting videos from the youtube here we will add category
         url(r'^add-video-details/?$','edit_selected_video',name='staff_video_edit_selected_video'),
         #url(r'^save-edited/?$',save_edited,name='staff_video_save_edited'),  # after category selection it will work 
         
         url(r'save-status/?$','ajax_video_change_status',name='staff_video_change_status'),
         
         #Video Editing/Seo 
         url(r'ajax-video-edit/$','ajax_video_edit',name='staff_video_ajax_edit_video'),
         url(r'ajax-video-seo/?$','ajax_video_seo',name='staff_videos_ajax_video_seo'),
         url(r'^viewStats/(?P<id>\d+)/$','seo_center',name='staff_video_ajax_statics'),
          
         
         
         
    
          
        )