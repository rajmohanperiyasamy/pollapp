from django.conf.urls import patterns, url

urlpatterns = patterns('classifieds.staffviews',
    url(r'^/?$', 'list_classified', name='staff_classified_home'),
    url(r'^ajax/?$', 'ajax_list_classified', name='ajax_list_classified'),
    url(r'^ajax-state/?$', 'ajax_classified_state', name='ajax_classified_state'),
    url(r'^ajax-action/?$', 'ajax_classified_action', name='ajax_classified_action'),
    url(r'^change-status/?$', 'change_status_classified', name="staff_change_status_classified"),
    # ADD
    url(r'^add/$', 'add_classified', name='add_classified'),
    url(r'^update/(?P<id>\d+)/$', 'update_classified', name='update_classified'),
    url(r'^preview/(?P<id>\d+)/?$', 'preview_classified', name="staff_preview_classified"),
    
    url(r'^listingtype/$', 'classified_listing_type', name='staff_classified_listing_type'),
    url(r'^seo/(?P<id>\d+)/$', 'seo', name='staff_classified_seo'),
    url(r'^offline-payment/(?P<cid>\d+)/?$', 'classified_offline_payment', name="classified_offline_payment"),
    
    url(r'^manage-classified-enquiry/(?P<id>\d+)/$', 'manage_enquiry', name='staff_manage_classified_enquiry'),
    
    # COMMON FUNCTION
    url(r'^update-ajax-cat/$', 'ajax_get_sub_category', name='ajax_get_sub_category'),
    url(r'^update-ajax-cat-atr/$', 'ajax_get_category_attribute', name='ajax_get_category_attribute'),
    url(r'^autosuggesttag/$', 'auto_suggest_tag', name='auto_suggest_tag_classifieds'),
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' , name='classifieds_ajax_upload_photos'),
#     url(r'^defaultphotos/$', 'ajax_get_default_photos' , name='classifieds_ajax_get_default_photos'),
#     url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' , name='classifieds_ajax_delete_photos'),
    # ABUSE
    # url(r'^abuse/?$','abuse',name='abuse'),
    # url(r'^abuse/filterby/?$','filter_by',name='filter_by'),
    # url(r'^bulkactions/?$','bulk_action',name='bulk_action'),
    # IMPORT/EXPORT
    url(r'export-csv/?$', 'classifieds_export_csv', name="staff_classifieds_export_csv"),
    url(r'import-csv/?$', 'classifieds_import_csv', name="staff_classifieds_import_csv"),
)


