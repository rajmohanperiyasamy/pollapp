from django.conf.urls import patterns, url

urlpatterns = patterns('payments.authorizenet.views',
     url(r'^sim/payment/$', 'sim_payment', name="authnet_sim_payment"),
)
