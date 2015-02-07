from django.conf.urls import *

urlpatterns = patterns('movies.views',
         # url(r'^twitter/?$','twitter_home',name='movies_home'),           
          url(r'^/?$','movies_home',name='movies_home_page'),   
          url(r'^addtofav/?$', 'movie_add_to_fav',name="movie_add_to_fav"),#need to remove #UNUSED
          
          url(r'^auto-suggest-movies/?$','auto_suggest_movies',name='movies_auto_suggest_movies'),
          #url(r'^search/','movies_search', name='movies_movies_search'),
          url(r'^ajax-update-movie-views/?$', 'update_movie_view_count',name="movies_update_movie_views"),
          
          url(r'^showtimes/search/$','showtime_search', name='showtime_search'),
          url(r'^trailers/$','movies_trailer_list', name='movies_movies_trailer_list'),
          url(r'^galleries/$','movies_galleries_list', name='movies_movies_galleries_list'),
          
          url(r'^showtimes/$','movies_showtimes', name='movies_movie_showtimes'),
          
          url(r'^showtimes/details/$','movies_showtime_details', name='movies_showtim_details'),
          url(r'^ajax_get_showtime_by_date/','get_showtimes_by_date', name='movies_get_showtimes_by_date'),
          
          url(r'^theater/showtimes/$', 'theater_showtimes', name='movies_theater_showtimes'),
          url(r'^ajax_get_theater_showtimes/','theater_showtimes_by_date', name='movies_ajax_theater_showtimes_by_date'),
          url(r'^theater/(?P<slug>[-\w]+)\.html/?$','theater_details', name='movies_theater_details'),
          url(r'^ajax_get_recent_reviews/','movies_recent_reviews', name='movies_get_recent_reviews'),
          
          url(r'^(?P<slug>[-\w]+)\.html/?$','movies_details',name='movies_details'),
          url(r'^(?P<movietype>[-\w]+)/$', 'movies_listing', name="movies_listing"),
                      
       )
