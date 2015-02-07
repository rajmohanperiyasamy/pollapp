from django.conf.urls import *

urlpatterns = patterns('deal.staffviews',
    
    url(r'^/?$', 'list_deals', name='staff_deals_home'),
    url(r'^ajax-listDeals/$', 'ajax_list_deals', name="staff_deals_ajax_list_deals"),
    url(r'^ajax-action/?$','ajax_deal_action',name='staff_deals_ajax_action'),
    url(r'^ajax-dealsstate/$', 'ajax_deal_state', name='staff_deals_ajax__state'),
    url(r'^ajax-voucher_details/$','voucher_details', name='staff_deals_voucher_details'),
    
    url(r'^add/$', 'add_deal', name='staff_deals_add_deal'),
    url(r'^business-autosuggest/$', 'address_autosuggest', name='staff_deal_address_suggest'),
    url(r'^merchant-autosuggest/$', 'merchant_autosuggest', name='staff_deal_merchant_suggest'),
    url(r'^get_business_address/$', 'get_address', name='staff_deal_get_address'),
    url(r'^add-business/$', 'add_address', name='staff_deal_add_address'),

    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='staff_deal_ajax_upload_photos'),
    url(r'^defaultphotos/$', 'ajax_get_default_photos' ,name='staff_deal_ajax_get_default_photos'),
    url(r'^ajaxdeletephoto/(?P<pk>\d+)$', 'ajax_delete_photos', name="staff_deal_delete_photos"),
    
    url(r'^seo/(?P<id>\d+)/$','seo',name='staff_deal_seo'), 
    url(r'^changestatus/$', 'change_status', name='staff_deal_change_status'),
    url(r'^ajax-feature/$', 'feature_deal', name='staff_deal_feature_deal'),
    
    url(r'^preview/(?P<id>\d+)/?$', 'deal_preview',name="staff_deal_preview"),
    url(r'^voucher_details/$', 'voucher_details', name='staffdeal_voucher_details'),
)

