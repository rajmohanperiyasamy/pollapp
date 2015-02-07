from django.conf.urls import patterns, url

urlpatterns = patterns('restaurants.views',
   url(r'^/?$', 'restaurants_home', name='restaurants_restaurants_home'),  
   url(r'^listing/$', 'list_restaurants_by_types', name='restaurants_list_restaurants_by_types'),
   url(r'^ajax-get-selected-values/$', 'restaurants_get_selected_values', name='restaurants_get_selected_values'),
   url(r'^ajax-filter-restaurants/$', 'ajajx_restaurants_listing', name='restaurants_filter_restaurants'),
   url(r'^auto-suggest-restaurants/$', 'auto_suggest_restaurants', name='restaurants_auto_suggest_restaurants'),
   url(r'^auto-suggest-locations/$', 'auto_suggest_restaurant_locations', name='restaurants_auto_suggest_restaurant_locations'),
   url(r'^ajax-menus-by-types/$', 'retrieve_menus_by_type', name='restaurants_retrieve_menus_by_type'),
   url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'restaurant_details', name="restaurants_restaurant_details"),
   url(r'^(?P<cuisineslug>[-\w]+)/$', 'restaurants_listing', name="restaurants_restaurants_listing"),
)