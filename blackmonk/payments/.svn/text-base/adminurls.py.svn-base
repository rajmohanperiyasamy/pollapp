from django.conf.urls import patterns, url, include
urlpatterns = patterns('payments.adminviews',
    url(r'^/?$', 'configuration_payment', name='admin_configuration_payment'),
    url(r'^update/?$', 'configuration_payment', name='admin_configuration_payment_update'),
    url(r'^stripe/', include('payments.stripes.adminurls')),
)
