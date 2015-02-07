from django.conf.urls import patterns, url

urlpatterns = patterns('hotels.views',
   url(r'^/?$', 'hotels_home', name='hotels_home'),  
   url(r'^ajax-tell-a-friend/$', 'ajax_tell_a_friend', name='hotels_ajax_tell_a_friend'),
   url(r'^search/$', 'hotel_search', name='hotels_hotel_search'),
   url(r'^ajax-autosuggest-hotels/$', 'hotel_auto_suggest', name='hotels_hotel_auto_suggest'),
   url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'hotel_details', name="hotel_details"),
   url(r'^(?P<catslug>[-\w]+)/$', 'hotels_home', name="hotels_home_category"),
)


