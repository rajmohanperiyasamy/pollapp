from django.conf.urls import patterns, url

urlpatterns = patterns('business.staffviews', 
    #BUSINESS
    url(r'^/?$', 'manage_business', name='staff_manage_business'),
    url(r'^ajax/?$','ajax_list_business',name='ajax_list_business'), 
    url(r'^ajax-action/?$','ajax_business_action',name='ajax_business_action'),
    url(r'^ajax-state/?$', 'ajax_business_state',name="ajax_business_state"),
    url(r'^change-status/?$', 'change_status_business',name="staff_change_status_business"),
    url(r'^seo/(?P<id>\d+)/?$', 'seo_business',name="staff_seo_business"),
    url(r'^listingtype/$', 'business_listing_type',name='staff_business_listing_type'), 
    
    url(r'^ajax-list-claim/$', 'ajax_list_business_claim',name='staff_ajax_list_business_claim'),
    url(r'^ajax-list-claim-status/$', 'ajax_list_business_claim_status',name='staff_ajax_list_business_claim_status'),
    url(r'^ajax-biz-unsubscription/$', 'ajax_biz_unsubscription',name='staff_ajax_biz_unsubscription'),
    
    url(r'^add/$', 'add_business', name='staff_add_business'),
    url(r'^update/(?P<id>\d+)/$', 'update_business', name='staff_update_business'),
    
    url(r'^preview/(?P<id>\d+)/?$', 'preview_business',name="staff_preview_business"),
    url(r'^images/(?P<id>\d+)/?$', 'business_images',name="staff_business_images"),
   
    url(r'^product/(?P<id>\d+)/?$', 'business_product',name="staff_business_product"),
    url(r'^product-add/(?P<bid>\d+)/?$', 'business_update_product',name="staff_business_product_add"),
    url(r'^product-update/(?P<bid>\d+)/(?P<id>\d+)/?$', 'business_update_product',name="staff_business_product_update"),
    url(r'^product-delete/?$', 'business_delete_product',name="staff_business_product_delete"),
    url(r'^product-load/?$', 'business_product_load_html',name="staff_business_product_load_html"),

    url(r'^coupon/(?P<id>\d+)/?$', 'business_coupon',name="staff_business_coupon"),
    url(r'^coupon-add/(?P<bid>\d+)/?$', 'business_update_coupon',name="staff_business_coupon_add"),
    url(r'^coupon-update/(?P<bid>\d+)/(?P<id>\d+)/?$', 'business_update_coupon',name="staff_business_coupon_update"),
    url(r'^coupon-delete/?$', 'business_delete_coupon',name="staff_business_coupon_delete"),
    url(r'^coupon-load/?$', 'business_coupon_load_html',name="staff_business_coupon_load_html"),
    
    url(r'^address/(?P<id>\d+)/?$', 'business_address',name="staff_business_address"),
    url(r'^address-add/(?P<bid>\d+)/?$', 'business_update_address',name="staff_business_address_add"),
    url(r'^address-update/(?P<bid>\d+)/(?P<id>\d+)/?$', 'business_update_address',name="staff_business_address_update"),
    url(r'^address-delete/?$', 'business_delete_address',name="staff_business_address_delete"),
    
    
    url(r'^manage-business-enquiry/(?P<id>\d+)/$', 'manage_enquiry', name='staff_manage_business_enquiry'),
    
    #COMMON FUNCTION
    url(r'^add-attributes/$', 'ajax_load_attribute', name='business_ajax_load_attribute'),
    url(r'^auto-suggest-tags/$', 'auto_suggest_tag', name='business_auto_suggest_tag'),
    url(r'^ajaxuploadfiles/$', 'ajax_upload_files' ,name='business_ajax_upload_files'),
    url(r'^deletefiles/(?P<pk>\d+)/$', 'business_delete_files', name='business_delete_files'),
    url(r'^ajaxuploadlogo/$', 'ajax_upload_logo' ,name='business_ajax_upload_logo'),
    url(r'^deletelogo/(?P<pk>\d+)/$', 'business_delete_logo', name='business_delete_logo'),
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='business_ajax_upload_photos'),
    url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='business_ajax_delete_photos'),
    url(r'^product-uploadphoto/$', 'ajax_upload_product_photo' ,name='business_ajax_upload_product_photo'),
    url(r'^product-deletephoto/(?P<pk>\d+)/$', 'business_delete_product_photo', name='business_delete_product_photo'),
    url(r'^coupon-uploadphoto/$', 'ajax_upload_coupon_photo' ,name='business_ajax_upload_coupon_photo'),
    url(r'^coupon-deletephoto/(?P<pk>\d+)/$', 'business_delete_coupon_photo', name='business_delete_coupon_photo'),
    url(r'^ajaxuploadcoverphotos/$', 'ajax_upload_cover_photos' ,name='business_ajax_upload_cover_photos'),
    
    url(r'^import-csv','business_import_csv',name="staff_business_import_csv"),
    url(r'^export-csv','business_export_csv',name="staff_business_export_csv"),
)


