from django.conf.urls import patterns, url

urlpatterns = patterns('deal.adminviews',
    url(r'^/?$', 'deals_settings', name='admin_portal_deals'),
    url(r'^settings/?$', 'deals_settings', name='admin_portal_deals_approval'),
    
    url(r'^category/?$', 'deals_category', name='admin_portal_deals_category'),
    url(r'^updatecategory/?$', 'deals_category_update', name='admin_portal_deals_category_update'),
    url(r'^deletecategory/?$', 'deals_category_delete', name='admin_portal_deals_category_delete'),

    url(r'^faq/?$', 'deals_faq', name='admin_portal_deals_faq'),
    url(r'^addfaq/?$', 'deals_add_faq', name='admin_portal_deals_add_faq'),
    url(r'^deletefaq/?$', 'deals_faq_delete', name='admin_portal_deals_faq_delete'),
    
    url(r'^howitwork/?$', 'deals_how', name='admin_portal_deals_how'),
    url(r'^update-description/?$', 'update_dcrptn', name='admin_portal_deals_update_dcrptn'),
    url(r'^add-howitwork/?$', 'deals_how_add', name='admin_portal_deals_add_howit'),
    url(r'^deletehow/?$', 'deals_how_delete', name='admin_portal_deals_how_delete'),
    
    
)