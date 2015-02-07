from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import *
#from sampleapp.views import date_and_time,templat,tempp, url_info, display, form, search, validation, sam, message
from common import staffviews

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    url(r'^/?$',staffviews.modules_data,name='staff_dashboard_content'),  
    url(r'^user_stats/$',staffviews.users_info),
    
    url(r'^feature-test/$', staffviews.feature_test, name='staff_feature_test'),
    url(r'^autosuggest-modlnms/$', staffviews.auto_sgt_moduls, name='staff_feature_auto_sgt_moduls'),
    url(r'^display-sgtdmodule/$', staffviews.dsply_sgstd_module, name='staff_feature_dsply_sgstd_module'),
    url(r'^save-content/$', staffviews.save_featured_content, name='staff_feature_save_featured_content'),
   
    url(r'^ajax-todo-list/$', staffviews.ajax_todo_lists, name='staff_ajax_todo_list'),
    url(r'^ajax-notification/$', staffviews.ajax_staff_notification, name='staff_ajax_notification'),
    url(r'^reset-notification/$', staffviews.reset_notification, name='staff_reset_notification'),
    
    ###enquiry urls####
    url(r'^ajax-enquiry/?$', staffviews.ajax_list_enquiry, name='ajax_list_enquiry'),
    url(r'^ajax-enquiry-action/?$', staffviews.enquiry_action, name='staff_enquiry_action'),
    url(r'^ajax-enquiry-detail/(?P<id>\d+)/?$', staffviews.enquiry_detail, name='staff_enquiry_detail'),
   
   
    url(r'^csvfile/delete/(?P<pk>\d+)/$',
        staffviews.DeleteCSVfile.as_view(),
        name='csvfile_delete'
    ),
    url(r'^csvfile/log/(?P<pk>\d+)/$',
        staffviews.PreviewCSVfileLog.as_view(),
        name='csvfile_log'
    ),
)

                            