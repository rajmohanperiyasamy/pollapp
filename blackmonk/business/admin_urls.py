from django.conf.urls import patterns, url

urlpatterns = patterns('business.adminviews',
    url(r'^/?$', 'business_setting', name='admin_portal_business'),
    url(r'^settings/?$', 'business_setting', name='admin_portal_business_approval'),
    
    url(r'^category/?$', 'business_category', name='admin_portal_business_category'),
    url(r'^updatecategory/?$', 'business_category_update', name='admin_portal_business_category_update'),
    url(r'^deletecategory/?$', 'business_category_delete', name='admin_portal_business_category_delete'),
    url(r'^seocategoryupdate/?$', 'business_seo_category_update', name='admin_portal_business_seo_category_update'),
    #Business Attributes Group
    url(r'^attributegroup/?$', 'business_attribute_group', name='admin_portal_business_attribute_group'),
    url(r'^updateattributegroup/?$', 'business_attribute_group_update', name='admin_portal_business_attribute_group_update'),
    url(r'^deleteattributegroup/?$', 'business_attribute_group_delete', name='admin_portal_business_attribute_group_delete'),
    #Business Attributes
    url(r'^attributes/?$', 'business_attributes', name='admin_portal_business_attributes'),
    url(r'^attributes-load/?$', 'business_attributes_load', name='admin_portal_business_attributes_load'),
    url(r'^updateattributes/?$', 'business_attributes_update', name='admin_portal_business_attributes_update'),
    url(r'^deleteattributes/?$', 'business_attributes_delete', name='admin_portal_business_attributes_delete'),
    url(r'^ajax-deleteattributes/?$', 'ajax_business_attribute_values_delete', name='ajax_admin_portal_business_attributevalues_delete'),
    #Business Payment Options
    url(r'^paymentoptions/?$', 'business_paymentoptions', name='admin_portal_business_paymentoptions'),
    url(r'^updatepaymentoptions/?$', 'business_paymentoptions_update', name='admin_portal_business_paymentoptions_update'),
    url(r'^deletepaymentoptions/?$', 'business_paymentoptions_delete', name='admin_portal_business_paymentoptions_delete'),
    #Business Pricing
    url(r'^pricing/$', 'business_price', name='admin_portal_business_price'),
    url(r'^sponsoredpricing/?$', 'business_sponsored_price', name='admin_portal_business_sponsored_price'),
    
)