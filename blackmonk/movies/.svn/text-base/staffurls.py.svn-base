from django.conf.urls import *

urlpatterns = patterns('movies.staffviews',
                       
            url(r'^/?$','movie_listing',name='staff_movie_listing'),
             
            url(r'^displayMovies/?$', 'movie_listing', name='staff_display_movie'),
            url(r'^ajax_displayMovie/?$', 'ajax_display_movie', name='staff_movie_ajax_display_movie'),
            url(r'^ajax-action/?$','ajax_movie_action',name='staff_movie_ajax_action'),
            url(r'^ajax-movie-sidebar/?$','ajax_movie_state',name='movie_staff_ajax__state'),
            url(r'^addmovie/?$','add_movie_details',name='movie_staff_addmovie'),
             
             
            url(r'^moviepreview/?$','movie_preview',name='staff_movie_preview_url'),
             
            url(r'^ajaxuploadphotos/?','ajax_upload_photos',name='staff_movie_ajax_photo_upload'),
            url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='movies_ajax_delete_photos'),
             
             
            url(r'^changestatusmovie/?$', 'ajax_change_status' ,name='staff_movie_change_status'),
            
            url(r'^editmovie/?$','edit_movie_detail',name='staff_movie_edit_movie'),
            url(r'^ajax-movie-seo/?$','ajax_movie_seo',name='staff_movie_ajax_movie_seo'),
            url(r'^ajax-upload-picture/?$','upload_pic',name='staff_movie_ajax_upload_pic'),
            url(r'^ajax-add-showtime/?','add_showtimes',name='staff_movie_ajax_add_showtime'),
            url(r'^add-movie-showtime/?$', 'add_movie_show_details', name='staff_movies_more_movie_show_details'),
            url(r'^edit-movie-showtime/?','edit_showtime_movie',name='staff_movie_edit_showtime_ajax'),
            url(r'^update-movie-showtime/?$','update_movie_ajax_showtime',name="staff_update_movie_ajax_showtime"),
            url(r'^delete-movie-showtimes/?$', 'delete_movie_showtime', name='staff_movies_delete_movie_showtime'),
            url(r'^addmoviecritics/?$','add_movie_critic_review',name='movie_ajax_add_critics'),
            url(r'^edit-critics-reviews/?$','edit_critics_reviews_ajax',name='staff_movie_edit_critic'),
            url(r'^delete-movie-review/?$','delete_movie_review', name='staff_movies_delete_movie_review'),
        
            
            url(r'^theatre-listing/?$','theatre_listing',name='staff_theatre_listing'),
            url(r'^staff_theatre_preview/?$','theatre_preview',name='staff_theatre_preview'),
            url(r'^staff_theatre_showtime-add/?$','add_theatre_showtime',name='staff_theatre_ajax_add_showtime'),
            url(r'^staff-theatre-saveshowtime/?$','save_theatre_showtime',name='staff_theatre_ajax_save_showtime'),
          
            url(r'^editshowdetails-theatre/?$', 'edit_theatre_showtime', name='staff_theatre_edit_show_details'),
            url(r'^savetheatreshow/?$','save_edit_theatre_show',name='staff_update_theatre_ajax_showtime'),
            url(r'^delete-theatre-showtimes/?$', 'delete_theatres_showtime', name='staff_movies_delete_theatre_showtime'),
           
            url(r'^displayTheatre/?$','ajax_display_theatre',name='staff_theatre_ajax_display_theatre'),
            url(r'^addtheatre/?','add_theatre_ajax',name='staff_movie_add_theatre_colorbox'),
            url(r'^addtheatreimage/?','image_upload',name='staff_movie_add_theatre_image_upload'),
            url(r'^uploadtheatreimage/?','add_theatre_pic',name='staff_theatre_upload_theatre'),
            url(r'^ajax-theatre-seo/?$','ajax_theatre_seo',name='staff_movie_ajax_theatre_seo'),
          
            url(r'^theatre-action','theatre_action',name='staff_theatre_ajax_action'),
            url(r'^edit-theatre','edit_theatre',name='staff_movie_edit_theatre'),
                        
                       
                          
        )