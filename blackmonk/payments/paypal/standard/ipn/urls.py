from django.conf.urls import *

urlpatterns = patterns('payments.paypal.standard.ipn.views',            
    url(r'^$', 'ipn', name="paypal-ipn"),
)