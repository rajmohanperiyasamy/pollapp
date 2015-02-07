from django.conf.urls import patterns, url

urlpatterns = patterns('payments.staffviews', 
    url(r'^/?$', 'view_payment_history', name='staff_view_payment_history'),
    url(r'^ajax/?$', 'ajax_view_payment_history', name='staff_ajax_view_payment_history'),
    url(r'^ajax-offline-payment/(?P<id>\d+)/$','ajax_offline_payment',name="staff_ajax_offline_payment"),
)


