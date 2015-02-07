from django.conf.urls import *

urlpatterns = patterns('deal.userviews',
    url(r'^$', 'order_list', name='deal_order_list'),
    url(r'^deal_details/(?P<id>\d+)/?$', 'user_deal_order_details', name='deal_order_details'),
    url(r'^redeem-voucher/$', 'redeem_voucher', name='redeem_voucher'),
    url(r'^(?P<orders>[-\w]+)/?$', 'order_list', name='deal_voucher_list'),
)