from django.conf.urls import patterns, url

urlpatterns = patterns('bmshop.shop.adminviews',
                       
    url(r'^/?$', 'admin_settings', name='admin_bmshop_main_settings'),
    url(r'^update-settings/?$', 'update_admin_settings', name='admin_bmshop_update_main_settings'),
    url(r'^payment-settings/?$', 'payment_settings', name='admin_bmshop_payment_settings'),
    url(r'^shipping/?$', 'shipping_settings', name='admin_bmshop_shipping_settings'),
   
    url(r'^autoemail/?$', 'auto_suggest_email', name='admin_bmshop_auto_email'),
  
)