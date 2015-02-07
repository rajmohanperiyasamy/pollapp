from django.conf.urls import patterns, url

urlpatterns = patterns('gallery.views',
    url(r'^/?$', 'gallery_home', name='gallery_home'),
    url(r'^a/ajaxcategory/?$', 'ajax_gallery_lsiting', name="ajax_gallery_lsiting"),
    url(r'^(all)\/?$', 'gallery_home', name="gallery_all"),
    url(r'^a/likegallery/$', 'like_gallery', name="like_gallery"),
    url(r'^a/ajax-tell-a-friend/$', 'ajax_tell_a_friend', name='gallery_ajax_tell_a_friend'),
    url(r'^a/ajaxrelatedalbum/$', 'ajax_related_album', name="ajax_related_album"),
    url(r'^a/count/(?P<id>\d+)/$', 'gallery_count', name="gallery_count"),
    url(r'^addtofav/?$', 'gallery_add_to_fav',name="gallery_add_to_fav"),  
    
    url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'gallery_detail', name="gallery_detail"),
    url(r'^(?P<catslug>[-\w]+)/$', 'gallery_home', name="gallery_listing"),
    
    url(r'^a/gallery-search/?$', 'search_gallery', name='search_gallery'),
)           