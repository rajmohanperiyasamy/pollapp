from django.conf.urls import patterns, url

urlpatterns = patterns('classifieds.adminviews',
    url(r'^/?$', 'classifieds_settings', name='admin_portal_classifieds'),
    url(r'^settings/?$', 'classifieds_settings', name='admin_portal_classifieds_approval'),
    url(r'^validate-oodle-api/?$', 'validate_oodle_api', name='admin_validate_oodle_api'),
    
    url(r'^category/?$', 'classifieds_category', name='admin_portal_classifieds_category'),
    url(r'^updatecategory/?$', 'classifieds_category_update', name='admin_portal_classifieds_category_update'),
    url(r'^deletecategory/?$', 'classifieds_category_delete', name='admin_portal_classifieds_category_delete'),
    url(r'^category-update-seo/?$', 'classifieds_seo_category_update', name='admin_portal_classifieds_seo_category_update'),
    #Classifieds Attributes
    url(r'^attributes/?$', 'classifieds_attribute', name='admin_portal_classifieds_attribute'),
    url(r'^attributes-load/?$', 'classifieds_attributes_load', name='admin_portal_classifieds_attributes_load'),
    url(r'^updateattributes/?$', 'classifieds_attribute_update', name='admin_portal_classifieds_attribute_update'),
    url(r'^deleteattributes/?$', 'classifieds_attribute_delete', name='admin_portal_classifieds_attribute_delete'),
    #Classifieds Pricing
    url(r'^pricing/$', 'classifieds_price', name='admin_portal_classifieds_price'),
    url(r'^sponsoredpricing/?$', 'classifieds_sponsored_price', name='admin_portal_classifieds_sponsored_price'),
)