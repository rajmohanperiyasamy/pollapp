from django.conf.urls import patterns, url

urlpatterns = patterns('payments.userviews', 
    url(r'^/?$', 'view_payment_history', name='user_view_payment_history'),
    url(r'^ajax/?$', 'ajax_view_payment_history', name='user_ajax_view_payment_history'),
    url(r'^details/(?P<id>\d+)/$','ajax_payment_details',name='ajax_payment_details'),
    url(r'^business_unsubscribe/(?P<id>\d+)/?$','business_unsubscribe',name='business_unsubscribe'),
    url(r'^update-my-card/(?P<id>\d+)/$', 'update_stripe_card_detail', name='update_stripe_card_detail'),
)


