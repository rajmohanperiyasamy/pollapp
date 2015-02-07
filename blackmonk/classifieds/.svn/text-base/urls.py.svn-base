from django.conf.urls import patterns, url

urlpatterns = patterns('classifieds.views',
   url(r'^/?$', 'classified_home', name='classified_home'),  
   url(r'^count/(?P<id>\d+)/$', 'classified_count', name="classified_count"),
   url(r'^a/ajaxtellafriend/$', 'ajax_tell_a_friend', name='classifieds_ajax_tell_a_friend'),
   url(r'^a/contact/$', 'contact', name='classifieds_contact'),
   url(r'^a/autosuggest-cls/$', 'auto_suggest_classifieds', name='auto_suggest_classifieds'),
   url(r'^addtofav/?$', 'classifieds_add_to_fav',name="classifieds_add_to_fav"), 
   url(r'^tp/(?P<id>[0-9]+)/?$', 'tp_classified', name='tp_classified_list'),
   url(r'^search/$', 'classified_listing', name='classified_search'),
   url(r'^(?P<catslug>[-\w]+)/$', 'classified_listing', name='classified_listing'),
   url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'classified_detail', name='classified_detail'),
   
)


