from django.conf.urls import patterns, url


urlpatterns = patterns('restaurants.adminviews',
    url(r'^/?$', 'restaurants_settings', name='admin_portal_restaurants'),
    url(r'^settings/?$', 'restaurants_settings', name='admin_portal_restaurants_approval'),
    
    url(r'^category/?$', 'restaurants_category', name='admin_portal_restaurants_category'),
    url(r'^updatecategory/?$', 'restaurants_category_update', name='admin_portal_restaurants_category_update'),
    url(r'^deletecategory/?$', 'restaurants_category_delete', name='admin_portal_restaurants_category_delete'),
    #url(r'^category-update-seo/?$', 'restaurants_seo_category_update', name='admin_portal_restaurants_seo_category_update'),
    
    url(r'^mealtypes/?$', 'restaurants_mealtypes', name='admin_portal_restaurants_mealtypes'),
    url(r'^updatemealtypes/?$', 'restaurants_mealtypes_update', name='admin_portal_restaurants_mealtypes_update'),
    url(r'^deletemealtypes/?$', 'restaurants_mealtypes_delete', name='admin_portal_restaurants_mealtypes_delete'),
    
    
    
    url(r'^cuisines/?$', 'restaurants_cuisines', name='admin_portal_restaurants_cuisines'),
    url(r'^updatecuisines/?$', 'restaurants_cuisines_update', name='admin_portal_restaurants_cuisines_update'),
    url(r'^deletecuisines/?$', 'restaurants_cuisines_delete', name='admin_portal_restaurants_cuisines_delete'),
    
    url(r'^feature/?$', 'restaurants_feature', name='admin_portal_restaurants_feature'),
    url(r'^updatefeature/?$', 'restaurants_feature_update', name='admin_portal_restaurants_feature_update'),
    url(r'^deletefeature/?$', 'restaurants_feature_delete', name='admin_portal_restaurants_feature_delete'),
    
    
    url(r'^payment/?$', 'restaurants_payment', name='admin_portal_restaurants_payment'),
    url(r'^updatepayment/?$', 'restaurants_payment_update', name='admin_portal_restaurants_payment_update'),
    url(r'^deletepayment/?$', 'restaurants_payment_delete', name='admin_portal_restaurants_payment_delete'),
    
    url(r'^pricing/$', 'restaurants_price', name='admin_portal_restaurants_price'),
)

