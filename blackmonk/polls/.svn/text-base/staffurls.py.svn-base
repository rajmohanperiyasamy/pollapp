from django.conf.urls import *

urlpatterns = patterns('polls.staffviews',
    url(r'^/?$' , 'home' , name = "staff_polls_polls_list")  ,              
    url(r'^addPoll/$' , 'add_poll' ,name = "staff_polls_add_poll")  ,
    url(r'^ajax-listpolls/$' , 'ajax_list_polls' , name ="staff_polls_ajax_list_polls" ),
    url(r'^ajax-polls-state/$', 'ajax_polls_state', name="staff_polls_ajax_state"),
    url(r'^ajax-action/?$','ajax_polls_action',name='staff_polls_ajax_action'),
    url(r'^ajax-choice-delete/?$','ajax_delete_choice', name = "staff_polls_ajax_delete_choice"),
    url(r'^ajax-change-status/?$','change_status', name = 'staff_polls_change_status'),
    url(r'^preview/$', 'polls_preview', name='staff_polls_preview')
)