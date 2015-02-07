from django.conf.urls import patterns, url

urlpatterns = patterns('business.views',
    url(r'^/?$', 'business_home', name='business_home'),
    url(r'^count/(?P<id>\d+)/$', 'business_count', name="business_count"),
    
    url(r'^a/contactus/$', 'contact_us', name='business_contact_us'),
    url(r'^a/ajax-tell-a-friend/$', 'ajax_tell_a_friend', name='business_ajax_tell_a_friend'),
    
    url(r'^a/autosuggest-buz/$', 'auto_suggest_business', name='auto_suggest_business'),
    url(r'^a/autosuggest-buz-address/$', 'auto_suggest_business_address', name='auto_suggest_business_address'),
    url(r'^addtofav/?$', 'business_add_to_fav',name="business_add_to_fav"), 
    url(r'^a/autosuggest-geolocation/$', 'auto_suggest_geolocation', name='auto_suggest_geolocation'),
    
    url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'business_details', name="business_details"),
    url(r'^(?P<catslug>[-\w]+)/$', 'business_list', name="business_listing"),
    
)

