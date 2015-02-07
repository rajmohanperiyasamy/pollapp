from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import *
#from sampleapp.views import date_and_time,templat,tempp, url_info, display, form, search, validation, sam, message
from common import feedback_views
from common import advertise_views

#feedback
urlpatterns = patterns('',
     
   url(r'^feedback/?$',feedback_views.feedback_listing,name='staff_feedback_listing'),
   url(r'^feedback-sorts/?$',feedback_views.feedback_sort,name='feedback_sort'),  
   url(r'^feedback-delete/',feedback_views.feedback_delete,name='delete_feedback'),
   url(r'^feedback-search/?$',feedback_views.searching,name='feedback_search_results'),  
   url(r'^feedback-detail/(?P<id>[-\w]*)',feedback_views.feedback_details,name='feedback_details'),
   
)

#advertisment

urlpatterns += patterns('common.advertise_views',
     
   url(r'^advertisement/?$',advertise_views.advertisement_listing,name='staff_advertisement_listing'),
   url(r'^advertise-sort/?$',advertise_views.advertise_sort,name='advertise_sort'),  
   url(r'^delete-advertisement/',advertise_views.advertise_delete,name='delete_advertisement'),
   url(r'^advertisement-search/?$',advertise_views.searching,name='search_results'),  
   url(r'^advertisement-detail/(?P<id>[-\w]*)',advertise_views.advertisment_details,name='advertisment_details'),  
   url(r'^ajax-advertise-action/?$', advertise_views.ajax_advertise_action, name='ajax_advertisement_action'),  
   
   url(r'^contacts/?$',advertise_views.contacts_listing,name='staff_contacts_listing'),
   url(r'^contacts-sort/?$',advertise_views.contacts_sort,name='contacts_sort'),  
   url(r'^delete-contacts/',advertise_views.contacts_delete,name='delete_contacts'),
   url(r'^contacts-search/?$',advertise_views.contacts_searching,name='contacts_search_results'),  
   url(r'^contacts-detail/(?P<id>[-\w]*)',advertise_views.contacts_details,name='contacts_details'),  
   url(r'^ajax-contacts-action/?$', advertise_views.ajax_contacts_action, name='ajax_contacts_action'),
)
       