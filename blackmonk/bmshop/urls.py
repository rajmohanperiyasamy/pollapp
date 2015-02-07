from django.conf.urls import patterns,url,include



urlpatterns = patterns('bmshop.cart.views',
       
       url(r'^cart/?$', 'cart_view', name='bmshop_product_cart'),
       url(r'^add-to-cart/?$', 'add_cart', name='bmshop_product_add_to_cart'),  
       url(r'^update-quantity/?$', 'update_quantity', name='bmshop_product_update_quantity'),  
       url(r'^remove-cart/(?P<item_id>\d*)$', "remove_cart_item", name="bmshop_product_remove_cart_item"),
)

urlpatterns += patterns('bmshop.order.views',
       
       url(r'^checkout/address/(?P<cart_id>\d+)/?$', 'check_out', name='bmshop_product_check_out_with_cart'),
       url(r'^checkout/address/?$', 'check_out', name='bmshop_product_check_out'),
       url(r'^checkout/order/(?P<address_id>\d+)/?$', 'order_summery', name='bmshop_product_order_summery'),
       url(r'^remove-item/(?P<item_id>\d*)$', "remove_item", name="bmshop_product_item_remove"),
       
       url(r'^checkout/payment/?$', 'order_payment', name='bmshop_product_checkout_payment'),
       
) 
urlpatterns += patterns('bmshop.products.views',
         
       url(r'^/?$', 'home', name="bmshop_product_home"),
       url(r'^filter-products/?$', 'ajax_filter_products', name='bmshop_product_filter_products'),
       url(r'^search/?$', 'search', name='bmshop_product_search_products'),
       url(r'^(?P<slug>[-\w]+)(.html)/$', 'product_detail', name="bmshop_product_detail"),
       
       url(r'^(?P<catslug>[-\w]+)/$', 'product_category_list', name="bmshop_product_category_list"),
       url(r'^(?P<parent_slug>[-\w]+)/(?P<catslug>[-\w]+)/$', 'product_category_list', name="bmshop_product_subcategory_list"),
)   