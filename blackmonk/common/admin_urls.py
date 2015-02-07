from django.conf.urls import *
urlpatterns = patterns('common.adminviews',
    
    #CONFIGURATION 
    url(r'^/?$', 'configuration', name='admin_configuration'),
    url(r'^general/?$', 'configuration_general', name='admin_configuration_general'),
    url(r'^general-update/?$', 'configuration_general_update', name='admin_configuration_general_update'),
    url(r'^ajax-customdate/?$', 'load_customdate', name='admin_load_customdate'),
    url(r'^ajax-customtime/?$', 'load_customtime', name='admin_load_customtime'),
    url(r'^ajax-upload-logo/?$', 'config_ajax_upload_logo', name='admin_configuration_ajax_upload_logo'),
    url(r'^ajax-delete-logo/?$', 'config_ajax_delete_logo', name='admin_configuration_ajax_delete_logo'),
    url(r'^ajax-upload-fav/?$', 'config_ajax_upload_fav', name='admin_configuration_ajax_upload_fav'),
    url(r'^ajax-delete-fav/?$', 'config_ajax_delete_fav', name='admin_configuration_ajax_delete_fav'),
    url(r'^ajax-upload-iphone/?$', 'config_ajax_upload_iphonelogo', name='admin_configuration_ajax_upload_iphonelogo'),
    url(r'^ajax-delete-iphone/?$', 'config_ajax_delete_iphonelogo', name='admin_configuration_ajax_delete_iphonelogo'),
    
    #Utilities
    url(r'^ajax-clear-cache/?$', 'clear_website_cache', name='admin_configuration_clear_website_cache'),
    url(r'^ajax-update-index/?$', 'update_global_search_index', name='admin_configuration_update_global_search_index'),
    url(r'^uploadimageyui/$', 'upload_image_from_editor',name='admin_configuration_upload_from_editor'),
    
    #Site Emai Config
    url(r'^general/emailsettings/?$', 'configuration_site_email_settings', name='admin_configuration_site_email_settings'),
    url(r'^ajax-test-smtp-connection/?$', 'test_smtp_connection', name='admin_configuration_test_smtp_connection'),
    url(r'^ajax-update-smtp-config?$', 'update_smtp_email_settings', name='admin_configuration_update_smtp_email_settings'),
    
    url(r'^social-url-update/?$', 'configuration_social_url_update', name='admin_configuration_social_url_update'),
    
    url(r'^general/signup/?$', 'configuration_general_signup', name='admin_configuration_general_signup'),
    url(r'^general/signup-update/?$', 'configuration_general_signup_update', name='admin_configuration_general_signup_update'),
    
    url(r'^general/share-buttons/?$', 'share_buttons', name='admin_configuration_share_buttons'),
    url(r'^general/ajax-share-buttons/?$', 'ajax_share_buttons', name='admin_configuration_ajax_share_buttons'),
    
    url(r'^available-apps/?$', 'configuration_available_apps', name='admin_configuration_available_apps'),
    url(r'^available-apps-change-status/?$', 'configuration_available_apps_change_status', name='admin_configuration_available_apps_change_status'),
    
    url(r'^analytics/?$', 'configuration_analytics', name='admin_configuration_analytics'),
    url(r'^banners/', include('banners.adminurls')),#Banner Ads Management

    url(r'^advertisement/?$', 'configuration_general_advertisement', name='admin_configuration_advertisement'),
    url(r'^advertisement-update/?$', 'configuration_general_advertisement_update', name='admin_configuration_advertisement_update'),
    url(r'^map-marker/?$', 'configuration_map_marker', name='admin_configuration_map_marker'),
    url(r'^map-marker-update/?$', 'configuration_map_marker_update', name='admin_configuration_map_marker_update'),
    url(r'^report/?$', 'configuration_report', name='admin_configuration_report'),
    url(r'^report-update/?$', 'configuration_report_update', name='admin_configuration_report_update'),
    url(r'^payment/', include('payments.adminurls')),
#     url(r'^payment/?$', 'configuration_payment', name='admin_configuration_payment'),
#     url(r'^payment-update/?$', 'configuration_payment_update', name='admin_configuration_payment_update'),
    url(r'^general/comments/?$', 'configuration_general_comments', name='admin_configuration_general_comments'),
    url(r'^general/comments-update/?$', 'configuration_general_comments_update', name='admin_configuration_general_comments_update'),
   
    #Email Templates
    url(r'^emailtemplates/?$', 'emailtemplates', name='admin_configuration_emailtemplates'),
    url(r'^email_changestatus/?$', 'change_email_status', name='admin_configuration_emailtmp_change_status'),
    url(r'^savetemplate/?$', 'email_savetemplate', name='admin_configuration_save_emailtemplate'),
    url(r'^viewtemplate/?$', 'view_template', name='admin_configuration_view_emailtemplate'),     
     #API NEWS LETTER CONFIGURATION
    url(r'^newsletter/?$', 'newsletter_configuration', name='admin_api_newsletter_configuration'),
    url(r'^newsletter/ajax-update-newsletter/?$', 'update_newsletter_api_settings', name='admin_update_newsletter_api_settings'),   
    
    # Advertisement Section #
    url(r'^ajax-get-ads-content/?$', 'configuration_get_ads_content', name='admin_configuration_get_ads_content'),
    
    url(r'^misc/?$', 'manage_misc', name='admin_config_manage_misc'),
    #url(r'^things-to-do/?$', 'manage_things_to_do', name='admin_config_manage_things_to_do'),
    #url(r'^golf/?$', 'manage_golf', name='admin_config_manage_golf'),
    url(r'^add/?$', 'misc_add', name='admin_add_misc'),
    url(r'^update/(?P<id>\d+)/?$', 'misc_add', name='admin_update_misc'),
    url(r'^delete/(?P<id>\d+)/?$', 'misc_delete', name='admin_delete_misc'),
    #COMMENTS
    url(r'^manage-comment-settings/?$', 'manage_comment_settings', name='admin_config_manage_comment_settings'),
    url(r'^update-comment-settings/?$', 'update_comment_settings', name='admin_config_update_comment_settings'),
    url(r'^auto_suggest_user/?$', 'auto_suggest_user', name='auto_suggest_user'),
)