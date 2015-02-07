from django.conf.urls import *

urlpatterns = patterns('deal.views',
    
    #DEAL
    url(r'^/?$', 'deals_home', name='deal_deals_home'),
    url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'deal_details', name='deals_deal_details'),
    url(r'^ajax_nearestdeal_search/$', 'ajax_nearestdeal_search', name='deal_ajax_nearestdeal_search'),
    url(r'^confirmation/$', 'confirmation', name='deal_confirmation'),
    
    # Merchant Varification
    url(r'^redeem/$', 'redeem', name='deal_redeem'),
    url(r'^confirm_redeem/$', 'confirm_redeem', name='deal_confirm_redeem'),
    url(r'^ajax_subscribe/$', 'ajax_subscribe', name="deal_ajax_subscribe"),
    url(r'^invite/$', 'invite', name="deal_invite"),
    
    url(r'^ajax_tell_a_friend/$', 'ajax_tell_a_friend', name='deal_ajax_tell_a_friend'),
    
    url(r'^how_it_works/$', 'how', name='deal_how'),
    url(r'^faqs/$', 'faqs', name='deal_faqs'),
    url(r'^contact/$', 'contact', name='deal_contact'),
    
    #Account
    url(r'^ajaxpaymentdetail/$', 'ajax_payment_detail', name='deal_ajax_payment_detail'),
    url(r'^deal-unsubscribe/(?P<id>\d+)/','deal_unsubscribe',name="deal_unsubscribe"),
    url(r'^(?P<catslug>[-\w]+)/$', 'deals_home', name="deals_category_listing"),
)