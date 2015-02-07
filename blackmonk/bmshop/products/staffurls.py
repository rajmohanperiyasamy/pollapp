from django.conf.urls import patterns, url

urlpatterns = patterns('bmshop.products.staffviews',
                       
    url(r'^/?$', 'product_list', name='staff_bmshop_product_list'),
    url(r'^ajax-products/?$', 'ajax_products', name='staff_bmshop_ajax_products'),
    url(r'^ajax-state/$', 'ajax_products_state', name="staff_bmshop_ajax_state"),
    
    url(r'^preview/(?P<product_id>\d+)/?$', 'preview_product', name='staff_bmshop_preview_product'),
    
    url(r'^add/?$', 'add_product', name='staff_bmshop_add_product'),
    url(r'^edit/(?P<product_id>\d+)/?$', 'add_product', name='staff_bmshop_edit_product'),
    url(r'^clone/(?P<product_id>\d+)/?$', 'clone_product', name='staff_bmshop_clone_product'),
    
    url(r'^update/(?P<product_id>\d+)/property/?$', 'product_property', name='staff_bmshop_product_property'),
    url(r'^get-property/?$', 'ajax_get_property', name='staff_bmshop_ajax_get_property'),
    url(r'^update-property-group/(?P<product_id>\d+)/?$', 'update_product_properties', name='staff_bmshop_update_product_properties'),
   
    url(r'^changestatus/$', 'change_status', name='staff_bmshop_change_status'),
    url(r'^ajax-feature/$', 'feature_product', name='staff_bmshop_feature_product'),
    url(r'^seo/(?P<id>\d+)/$','seo',name='staff_bmshop_product_seo'), 
    
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='staff_bmshop_ajax_upload_photos'),
    url(r'^defaultphotos/$', 'ajax_get_default_photos' ,name='staff_bmshop_ajax_get_default_photos'),
    url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='staff_bmshop_ajax_delete_photos'),
    
    url(r'^property/?$', 'property_list', name='staff_bmshop_property_list'),
    url(r'^ajax-property/?$', 'ajax_property', name='staff_bmshop_ajax_property'),
    url(r'^addproperty/?$', 'add_property', name='staff_bmshop_add_property'),
    url(r'^editroperty/(?P<property_id>\d+)/?$', 'add_property', name='staff_bmshop_edit_property'),
    
    url(r'^propertygroup/?$', 'group_property_list', name='staff_bmshop_group_property_list'),
    url(r'^addpropertygrp/?$', 'add_property_group', name='staff_bmshop_add_property_group'),
    url(r'^ajax-group/?$', 'ajax_group', name='staff_bmshop_ajax_group'),
    
    
    
    
    
  
)