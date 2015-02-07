from django.conf.urls import patterns, url

urlpatterns = patterns('bmshop.products.adminviews',
                       
    url(r'^category/?$', 'category_settings', name='admin_bmshop_category_settings'),
    url(r'^update-category/?$', 'category_update', name='admin_bmshop_update_category'),
    url(r'^delete-category/?$', 'delete_category', name='admin_bmshop_delete_category'),
    
    url(r'^delivery-times/?$', 'delivery_time', name='admin_bmshop_delivery_time'),
    url(r'^update-dlvrytimes/?$', 'update_delivery_time', name='admin_bmshop_update_delivery_time'),
    url(r'^delete-dlvrytimes/?$', 'delete_delivery_time', name='admin_bmshop_delete_delivery_time'),
    
    url(r'^manufactures/?$', 'manufactures', name='admin_bmshop_manufactures'),
    url(r'^update-manufactures/?$', 'update_manufactures', name='admin_bmshop_update_manufactures'),
    url(r'^delete-manufactures/?$', 'delete_manufactures', name='admin_bmshop_delete_manufactures'),
  
)