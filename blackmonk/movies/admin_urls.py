from django.conf.urls import patterns, url

urlpatterns = patterns('movies.adminviews',
    url(r'^/?$', 'movies_settings', name='admin_portal_movies'),
    url(r'^settings/?$', 'movies_settings', name='admin_portal_movies_settings'),
    
    
    url(r'^genre/?$', 'movies_genre', name='admin_portal_movies_genre'),
    url(r'^updategenre/?$', 'movies_genre_update', name='admin_portal_movies_genre_update'),
    url(r'^deletegenre/?$', 'movies_genre_delete', name='admin_portal_movies_genre_delete'),
    
    url(r'^criticsource/?$', 'movies_criticsource', name='admin_portal_movies_criticsource'),
    url(r'^updatecriticsource/?$', 'movies_criticsource_update', name='admin_portal_movies_criticsource_update'),
    url(r'^deletecriticsource/?$', 'movies_criticsource_delete', name='admin_portal_movies_criticsource_delete'),
    
    url(r'^language/?$', 'movies_language', name='admin_portal_movies_language'),
    url(r'^updatelanguage/?$', 'movies_language_update', name='admin_portal_movies_language_update'),
    url(r'^deletelanguage/?$', 'movies_language_delete', name='admin_portal_movies_language_delete'),
   
    url(r'^seogenreupdate/?$', 'movies_seo_genre_update', name='admin_portal_movies_seo_genre_update'),
)