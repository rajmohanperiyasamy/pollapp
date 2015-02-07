from django.conf.urls import patterns,url,include


urlpatterns = patterns('bmshop.customer.userviews',
         
         url(r'^wishlist/?$', 'wishlist', name='bmshop_user_wish_list'),
         url(r'^add-wishlist/(?P<slug>[-\w]+)$', 'add_wishlist', name='bmshop_user_add_wish_list'),
         url(r'^delete-wishlist/?$', 'delete_wishlist', name='bmshop_user_delete_wishlist'),
 
)
urlpatterns += patterns('bmshop.order.userviews',
         
         url(r'^orders/?$', 'my_orders', name='bmshop_user_my_orders'),
         url(r'^ajax/?$', 'ajax_view_my_orders', name='bmshop_user_ajax_view_my_orders'),
 
)
urlpatterns += patterns('bmshop.cart.userviews',
         
         url(r'^addcart/?$', 'add_to_cart', name='bmshop_user_add_to_cart'),
 
)   