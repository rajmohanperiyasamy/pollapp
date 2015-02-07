from django.conf.urls import *
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
        url(r'^/?$','common.adminviews.dashboard',name='admin_home'),#PORTAL HOME
        url(r'^user/', include('usermgmt.admin_urls')),#Usermanagement
        url(r'^config/', include('common.admin_urls')),#Congiguration
        url(r'^design/', include('common.design_urls')),#Designs
        
        url(r'^reports/', 'common.adminviews.admin_reports', name="admin_report"),
        url(r'^custom-page/', include('common.page_urls')),#CUSTOM PAGE
        
        url(r'^portal/?$','common.adminviews.dashboard',name='admin_portal'),#PORTAL HOME
        url(r'^portal-seo-update/?$','common.adminviews.home_seo_update',name='admin_portal_home_seo_update'),
        url(r'^portal/community/',include('community.admin_urls')),#Community
        url(r'^portal/articles/',include('article.admin_urls')),#Articles
        url(r'^portal/attractions/',include('attraction.admin_urls')),#Attraction
        url(r'^portal/business/',include('business.admin_urls')),#Business
        url(r'^portal/bookmarks/', include('bookmarks.adminurls') ),#Bookmarks
        url(r'^portal/classifieds/',include('classifieds.admin_urls')),#Classifieds
        url(r'^portal/deals/',include('deal.admin_urls')),#Deals
        url(r'^portal/events/',include('events.admin_urls')),#Events
        #url(r'^portal/discussions/',include('forum.admin_urls')),#Forum 
        url(r'^portal/photos/',include('gallery.admin_urls')),#Gallery
        url(r'^portal/polls/',include('polls.admin_urls')),#Gallery
        url(r'^portal/locality/',include('locality.admin_urls')),#Locality
        url(r'^portal/meetups/', include('meetup.adminurls')),#Meetup
        url(r'^portal/movies/', include('movies.admin_urls')),#Movies
        url(r'^portal/news/',include('news.admin_urls')),#NEWS
        url(r'^portal/usermgmt/',RedirectView.as_view(url='/admin/users/')),#Manage User
        url(r'^portal/videos/', include('videos.admin_urls')), #Videos
        url(r'^portal/seo/', include('common.seo_urls')),#SEO SETTINGS
        url(r'^portal/jobs/', include('jobs.admin_urls')),#JOB PAGE
        url(r'^portal/sweepstakes/', include('sweepstakes.adminurls')),#sweepstakes
        url(r'^portal/', include('common.api_urls')),#API
        url(r'^portal/shop/', include('bmshop.adminurls')),#shop
        url(r'^portal/restaurants/', include('restaurants.adminurls')),#restaurants
)