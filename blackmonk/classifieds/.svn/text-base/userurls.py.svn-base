from django.conf.urls import patterns,url

urlpatterns = patterns('classifieds.userviews',
    url(r'^/?$','list_classified', name='user_classified_home'),
    url(r'^ajax/?$','ajax_list_classified',name='user_ajax_list_classified'),
    url(r'^ajax-state/?$','ajax_classified_state',name='user_ajax_classified_state'),
    url(r'^ajax-action/?$','ajax_classified_action',name='user_ajax_classified_action'),
    url(r'^upgrade-listingtype/(?P<id>\d+)/$', 'classified_upgrade_listing_type',name='user_classified_upgrade_listing_type'), 
    url(r'^seo/(?P<id>\d+)/$','seo',name='user_classified_seo'), 
    #ADD-EDIT
    url(r'^add/$', 'add_classified', name='user_add_classified'),
    url(r'^add-listing/(?P<id>\d+)/$', 'add_classifieds_listing',name='user_add_classifieds_listing'),
    url(r'^update-ajax-user-cat/$', 'ajax_get_user_sub_category', name='ajax_get_user_sub_category'), 
    #url(r'^update/(?P<id>\d+)/$', 'update_classified', name='user_update_classified'),
    url(r'^preview/(?P<id>\d+)/?$', 'preview_classified',name="user_preview_classified"),
    url(r'^update-ajax-user-cat-atr/$', 'ajax_get_user_category_attribute', name='ajax_get_user_category_attribute'),
)


