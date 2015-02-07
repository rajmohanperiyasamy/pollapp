from django.conf.urls import patterns, url

urlpatterns = patterns('locality.mapviews',
    url(r'^/?$', 'map_home', name='locality_map_home'),
    url(r'^business/?$','map_home',name='locality_map_business'), 
    url(r'^ajax-filter-business/?$','map_ajax_filter_business',name='locality_map_ajax_filter_business'), 
    
    url(r'^events/$','map_events',name='locality_map_events'), 
    url(r'^ajax-filter-events/?$','map_ajax_filter_events',name='locality_map_ajax_filter_events'), 
    
    url(r'^classifieds/$','map_classifieds',name='locality_map_classifieds'), 
    url(r'^ajax-filter-classifieds/?$','map_ajax_filter_classifieds',name='locality_map_ajax_filter_classifieds'),
    
    url(r'^cinemas/$','map_cinemas',name='locality_map_cinemas'), 
    url(r'^ajax-filter-cinemas/?$','map_ajax_filter_cinemas',name='locality_map_map_ajax_filter_cinemas'),
    
    url(r'^attractions/$','map_attractions',name='locality_map_attractions'), 
    url(r'^ajax-filter-attractions/?$','map_ajax_filter_attractions',name='locality_map_ajax_filter_attractions'),
    
    url(r'^direction/$','map_get_direction',name='locality_map_map_get_direction'),
    url(r'^ajax-direction/$','ajax_map_get_direction',name='locality_map_ajax_get_direction'),
    
)   