from django.conf.urls import patterns, url

urlpatterns = patterns('business.userviews', 
    #BUSINESS
    url(r'^/?$', 'manage_business', name='user_manage_business'),
    url(r'^ajax/?$','ajax_list_business',name='user_ajax_list_business'), 
    url(r'^ajax-action/?$','ajax_business_action',name='user_ajax_business_action'),
    url(r'^ajax-state/?$', 'ajax_business_state',name="user_ajax_business_state"),
    url(r'^seo/(?P<id>\d+)/?$', 'seo_business',name="user_seo_business"),
    url(r'^upgrade-listing/(?P<id>\d+)/$', 'business_upgrade_listing_type',name='user_business_upgrade_listing_type'), 
    
    url(r'^add/$', 'add_business', name='user_add_business'),
    url(r'^add-listing/(?P<id>\d+)/$', 'add_business_listing', name='user_add_business_listing'),
    url(r'^update/(?P<id>\d+)/$', 'update_business', name='user_update_business'),
    
    url(r'^preview/(?P<id>\d+)/?$', 'preview_business',name="user_preview_business"),
    url(r'^images/(?P<id>\d+)/?$', 'business_images',name="user_business_images"),
   
    url(r'^claim/(?P<id>\d+)/$', 'claim_business', name='user_claim_business'),
    
    url(r'^product/(?P<id>\d+)/?$', 'business_product',name="user_business_product"),
    url(r'^product-add/(?P<bid>\d+)/?$', 'business_update_product',name="user_business_product_add"),
    url(r'^product-update/(?P<bid>\d+)/(?P<id>\d+)/?$', 'business_update_product',name="user_business_product_update"),
    url(r'^product-delete/?$', 'business_delete_product',name="user_business_product_delete"),
#     url(r'^product-load/?$', 'business_product_load_html',name="user_business_product_load_html"),

    url(r'^coupon/(?P<id>\d+)/?$', 'business_coupon',name="user_business_coupon"),
    url(r'^coupon-add/(?P<bid>\d+)/?$', 'business_update_coupon',name="user_business_coupon_add"),
    url(r'^coupon-update/(?P<bid>\d+)/(?P<id>\d+)/?$', 'business_update_coupon',name="user_business_coupon_update"),
    url(r'^coupon-delete/?$', 'business_delete_coupon',name="user_business_coupon_delete"),
#     url(r'^coupon-load/?$', 'business_coupon_load_html',name="user_business_coupon_load_html"),
    
    url(r'^address/(?P<id>\d+)/?$', 'business_address',name="user_business_address"),
    url(r'^address-add/(?P<bid>\d+)/?$', 'business_update_address',name="user_business_address_add"),
    url(r'^address-update/(?P<bid>\d+)/(?P<id>\d+)/?$', 'business_update_address',name="user_business_address_update"),
    url(r'^address-delete/?$', 'business_delete_address',name="user_business_address_delete"),
    
    
    url(r'^ajax-listing-add-cat/$', 'ajax_listing_add_cat', name='business_listing_ajax_add_cat'),
    url(r'^ajax-listing-delete-cat/$', 'ajax_listing_delete_cat', name='business_listing_ajax_delete_cat'),
    
    url(r'^add-attributes/$', 'ajax_load_attribute', name='user_business_ajax_load_attribute'),
    url(r'^user_biz_get_part_html/?$', 'user_biz_get_part_html',name="user_biz_get_part_html"),
)


