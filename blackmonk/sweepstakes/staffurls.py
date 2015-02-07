from django.conf.urls import *

urlpatterns = patterns('sweepstakes.staffviews',
    url(r'^/?$', 'manage_sweepstakes',name="staff_manage_sweepstakes"),
    url(r'^ajax/?$','ajax_list_sweepstakes',name='ajax_list_sweepstakes'), 
    url(r'^ajax-action/?$','ajax_sweepstakes_action',name='ajax_sweepstakes_action'),
    url(r'^ajax-state/?$', 'ajax_sweepstakes_state',name="ajax_sweepstakes_state"),
    url(r'^seo/(?P<id>\d+)/?$', 'seo_sweepstakes',name="staff_seo_sweepstakes"),
    url(r'^change-status/?$', 'change_status_sweepstakes',name="staff_change_status_sweepstakes"),
    #ADD EDIT
    url(r'^add/?$', 'add_sweepstakes',name="staff_add_sweepstakes"),
    url(r'^update/(?P<id>\d+)/?$', 'edit_sweepstakes',name="staff_edit_sweepstakes"),
    url(r'^preview/(?P<id>\d+)/?$', 'preview_sweepstakes',name="staff_preview_sweepstakes"),
    
    #OFFER
    url(r'^offer-add/(?P<bid>\d+)/?$', 'sweepstakes_update_offer',name="staff_sweepstakes_offer_add"),
    url(r'^offer-update/(?P<bid>\d+)/(?P<id>\d+)/?$', 'sweepstakes_update_offer',name="staff_sweepstakes_offer_update"),
    url(r'^offer-delete/?$', 'sweepstakes_delete_offer',name="staff_sweepstakes_offer_delete"),
    url(r'^offer-load/?$', 'sweepstakes_offer_load_html',name="staff_sweepstakes_offer_load_html"),
    
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='staff_sweepstakes_ajax_upload_photos'),
    url(r'^ajaxuploadphotos-offer/$', 'ajax_upload_photos_offer' ,name='staff_sweepstakes_ajax_upload_photos_offer'),
    url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='staff_sweepstakes_ajax_delete_photos'),
)