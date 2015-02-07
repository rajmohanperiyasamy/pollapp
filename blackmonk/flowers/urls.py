from django.conf.urls import patterns, url

urlpatterns = patterns('flowers.views',
   url(r'^/?$', 'flowers_home', name='flowers_flowers_home'),  
   #url(r'^ajax-tell-a-friend/$', 'ajax_tell_a_friend', name='hotels_ajax_tell_a_friend'),
   url(r'^search/$', 'flowers_search', name='flowers_flowers_search'),
   url(r'^ajax-autosuggest-flowers/$', 'flowers_auto_suggest', name='flowers_flowers_auto_suggest'),
   url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'flower_details', name="flowers_flower_details"),
   url(r'^(?P<catslug>[-\w]+)/$', 'flowers_home', name="flowers_by_category"),
)


