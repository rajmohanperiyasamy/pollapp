from django.conf.urls import *
from django.views.generic import TemplateView
from payments.views import *
from payments.googlecheckout import urls as gc 

urlpatterns = patterns('',
    url(r'^(?P<moduleslug>[-\w]+)/success/$', payments_success, name='payments_success'),
    
    url(r'^business/confirm/(?P<bid>\d+)/(?P<lid>\d+)/$',business_payments_confirm,name='business_payments_confirm'),
    url(r'^banners/confirm/(?P<bid>\d+)/(?P<lid>\d+)/$',banners_payments_confirm,name='banners_payments_confirm'),
    url(r'^events/confirm/(?P<eid>\d+)/(?P<lid>\d+)/$',event_payments_confirm,name='event_payments_confirm'),
    url(r'^article/confirm/(?P<aid>\d+)/',article_payments_confirm,name='article_payments_confirm'),
    url(r'^classifieds/confirm/(?P<cid>\d+)/(?P<lid>\d+)/',classifieds_payments_confirm,name='classifieds_payments_confirm'),
    url(r'^deal/payment/(?P<did>\d+)/(?P<dpid>\d+)/$', deal_payment, name='deal_payment'),
    
    ##########Offline payment##############
    url(r'^banner/offline_confirm/(?P<bid>\d+)/(?P<lid>\d+)/$',banner_payments_offline_confirm,name='banner_payments_offline_confirm'),
    url(r'^article/offline_confirm/(?P<aid>\d+)/',article_payments_offline_confirm,name='article_payments_offline_confirm'),
    url(r'^events/offline_confirm/(?P<eid>\d+)/(?P<lid>\d+)/$',event_payments_offline_confirm,name='event_payments_offline_confirm'),
    url(r'^classifieds/offline_confirm/(?P<cid>\d+)/(?P<lid>\d+)/',classifieds_payments_offline_confirm,name='classifieds_payments_offline_confirm'),
    url(r'^business/offline_confirm/(?P<bid>\d+)/(?P<lid>\d+)/$',business_payments_offline_confirm,name='business_payments_offline_confirm'),
    
    (r'^paypal/notify/', include('payments.paypal.standard.ipn.urls')),
    (r'^gc/', include(gc)),
    (r'^authorizenet/', include('payments.authorizenet.urls')),
    url(r'^stripe/notify/', stripe_notify,name="stripe_notify"),
    url(r'^stripe/subscribers/', stripe_list_subscribers,name="stripe_subscribers"),
#     url(r'^stripe/add_subscription_plan/', stripe_add_plan,name="stripe_add_plan"),
#     url(r'^stripe/list_subscription_plans/', stripe_list_plans,name="stripe_list_plans"),
#     url(r'^stripe/plans/details/(?P<id>\d+)/', stripe_plan_details,name="stripe_plan_details"),
)