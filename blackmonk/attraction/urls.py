from django.conf.urls import patterns, url

urlpatterns = patterns('attraction.views',
                       
    url(r'^/?$', 'attractions_home', name='attraction_home'),
    url(r'^(?P<catslug>[-\w]+)/$', 'attractions_home', name="attraction_listing"),
    url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'attraction_details', name="attraction_detail"),
    
    url(r'^a/count/(?P<id>\d+)/?$', 'attraction_count', name='attraction_count'),
    #url(r'^a/autosuggest-attraction/$', 'auto_suggest_attraction', name='auto_suggest_attraction'),
    #url(r'^a/autosuggest-attraction-address/$', 'auto_suggest_attraction_address', name='auto_suggest_attraction_address'),
    
    url(r'^addtofav/?$', 'attraction_add_to_fav',name="attraction_add_to_fav"), 
    url(r'^a/get-nearby-items/$', 'get_nearby_items' ,name='attraction_get_nearby_items'),
    url(r'^a/ajaxuploadphotos/$', 'ajax_upload_photos' ,name='attraction_contribute_photos'),
    url(r'^a/attractionsearch/$', 'attraction_search' ,name='attraction-search'),
) 
