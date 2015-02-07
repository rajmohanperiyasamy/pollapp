from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

js_info_dict = {
    'packages': ('blackmonk',),
}

from django.conf import settings as mysettings 
urlpatterns = patterns('',
    
   (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),  
   (r'^admincp/', include(admin.site.urls)),
                     
   url(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': mysettings.MEDIA_ROOT}),
   #url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': mysettings.STATIC_ROOT}),
   
   url(r'^/?$', 'common.views.home', name='site_home'),
   
   url(r'^comments/', include('mptt_comments.urls')),
   
   url(r'^track/', include('analytics.urls')),
   url(r'^get_menu_id/?$', 'common.views.get_menu_id', name="get_menu_id"),
   url(r'^feedback/', 'common.views.feedback',name='feedback'),
   url(r'^admin/', include('blackmonk.adminurls')),
   url(r'^staff/', include('blackmonk.staffurls')),
   url(r'^user/', include('blackmonk.userurls')),
   url(r'^account/', include('usermgmt.urls')),
   url(r'^profile/',include('usermgmt.profileurls')),
   url(r'^twitter/', include('twitter_login.urls')),
   url(r'^openid/', include('openid_login.urls')),
   url(r'^fbconnect/', include('fbconnect.urls')),
   url(r'^linkedin/', include('linkedin.urls')),
   #url(r'^profile/',include('usermgmt.profileurls')),
   url(r'^search/', include('haystack.urls')),
   #Modules
   url(r'^articles/', include('article.urls')),
   url(r'^attractions/', include('attraction.urls')),
   url(r'^business/', include('business.urls')),
   url(r'^classifieds/', include('classifieds.urls')),
   url(r'^events/', include('events.urls')),
   #url(r'^discussions/', include('forum.urls')),
   url(r'^photos/', include('gallery.urls')),  
   url(r'^locality/', include('locality.urls')),
   url(r'^deals/', include('deal.urls')),
   url(r'^videos/', include('videos.urls')),
   url(r'^movies/', include('movies.urls')),
   url(r'^hotels/', include('hotels.urls')),
   url(r'^news/', include('news.urls')),
   url(r'^buzz/', include('buzz.urls')),
   #url(r'^weddings/', include('hotels.urls')),
   url(r'^restaurants/', include('restaurants.urls')),
   url(r'^bookmarks/', include('bookmarks.urls')),
   url(r'^community/', include('community.urls')),
   url(r'^florist/', include('flowers.urls')),
   url(r'^rss/', include('blackmonk.rssurls')),
   url(r'^meetups/', include('meetup.urls')),
   url(r'^jobs/', include('jobs.urls')),
   
   url(r'^shop/', include('bmshop.urls')),
   
   url(r'^venues/', include('events.venue_urls')),
   url(r'^polls/', include('polls.urls')),
   url(r'^banners/', include('banners.urls')),

   #url(r'^mobapp/', include('mobapp.urls')),
   
   url(r'^googlepluscount/$', 'common.views.get_google_plus_count'),
  
   #Coming Soon
   url(r'^jobs/', 'common.views.coming_soon'),
   url(r'^cruise/', 'common.views.coming_soon'),
   url(r'^golf/', 'common.views.golf'),
   #url(r'^nightlife/', 'common.views.coming_soon'),
   url(r'^flights/', 'common.views.coming_soon'),
   url(r'^places-to-see/', 'common.views.things_to_do'),
   url(r'^weddings/', 'common.views.weddings'),
   url(r'^reports/$', 'common.views.modules_elements_views'),
   url(r'^viewstats/(?P<id>\d+)/(?P<modules>\w+)/(?P<year>\d+)/$', 'common.views.get_modules_elements_views',name="common_get_modules_elements_views"),
   url(r'^viewsources/(?P<id>\d+)/(?P<modules>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<type>\w+)/$', 'common.views.get_traffic_sources',name="get_traffic_sources"),  
   

   #Contact,Advertise
   url(r'^advertise/$', 'common.views.advertise', name='common_advertise'), 
   url(r'^contact/$', 'common.views.contact', name='common_contact'),
   
   url(r'^contest/', include('sweepstakes.urls')),
   url(r'^sweepstakes/', include('sweepstakes.urls')), 
   
   #Pages
   url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'common.views.resources', name="resources"),
   url(r'^(?P<slug>[-\w]+)(.png)\/?$', 'common.views.favicon', name="favicon"),
   url(r'^robots.txt/?$', 'common.views.robot_txt', name="robot_txt"),
   #Payment
   url(r'^payments/', include('payments.urls')),  
   
   #Weather
   url(r'^weather/$', 'common.views.weather', name='common_weather'), 
   
   #map
   url(r'^map/', include('locality.mapurls')), 
   
   #Banner Ads 
   url(r'^ajax-get-banner/?$', 'common.views.get_banner_ads', name='common_get_banner_ads'),
   
   #User Navigation Site Map
   url(r'^sitemap/', 'common.views.sitemap',name='sitemap'), 
   
   #STAFF TOUR
   url(r'^bmt/(.*)$', 'django.views.static.serve', {'document_root': mysettings.MEDIA_TOUR_ROOT}),
   
   #FAVICON
   url(r'^favicon.ico$', 'common.views.favicon', name='favicon'), 
   
   #CHANNELS
   url(r'^(?P<channel_slug>[-\w]+)/', include('channels.urls')),
   )
urlpatterns += patterns('',
    (r'^sitemap\.xml$', 'common.config_sitemaps.index'),
    (r'^google-news\.xml$', 'common.config_sitemaps.google_news_sitemap'),
    (r'^sitemap-(?P<section>.+)\.xml$', 'common.config_sitemaps.sitemap'),
) 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
