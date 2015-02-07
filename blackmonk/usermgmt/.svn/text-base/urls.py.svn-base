from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('usermgmt.views',
    
    # Authentication Section #
    
    url(r'^ajax_auth_close_popup/?$','ajax_auth_close_popup', name='ajax_auth_close_popup'),
    url(r'^newsletter-subscription','ajax_newsletter',name='ajax_newsletter_url'),
  
    # Registration #
    url(r'^signup/?$', 'sign_up', name='user_signup'),
    url(r'^ajax-signin/?$', 'ajax_signin', name='ajax_signin'),
    url(r'^ajax-signup/?$', 'ajax_signup', name='ajax_signup'),
    
    url(r'^password/$', 'change_password',name='usermgmt_password_change'),
    url(r'^forgotpwd/$', 'forgotpwd', name='usermgmt_forgotpwd'),    
    url(r'^retrivepwd/(?P<code>\w+)/(?P<email>\w+)/(?P<id>\d+)/$', 'retrive_password', name='retrive_password'),  
    
    
    url(r'^profile/?$', 'user_profile', name='usermgmt_viewprofile'),
    
    url(r'^profile/invite/?$', 'user_invite', name='usermgmt_user_invite'),
    url(r'^profile/invite-load-more/?$', 'user_invite_google_more', name='usermgmt_user_invite_google_more'),
    url(r'^profile/invite-mail/?$', 'user_invite_mail', name='usermgmt_user_invite_mail'),
    
    url(r'^ajax-update-profile/$', 'update_profile', name='usermgmt_ajax_update_profile'),
    url(r'^ajax-update-email/$', 'update_email', name='usermgmt_ajax_update_email'),
    url(r'^ajax-social-profiles/$', 'add_social_profiles', name='usermgmt_ajax_add_social_profiles'),
    url(r'^ajax-delete-profiles/$', 'delete_social_profiles', name='usermgmt_ajax_delete_social_profiles'),
    url(r'^ajax-update-social-profiles/$', 'update_social_profiles', name='usermgmt_ajax_update_social_profiles'),
    
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='usermgmt_ajax_upload_photos'),
    url(r'^ajaxdeletephotos/(?P<pk>\d+)$', 'ajax_delete_photos' ,name='usermgmt_ajax_delete_photos'),
    
    url(r'^userstatus/$', 'user_status', name='ajax_user_status'),
    
    #contact
    url(r'^contact-info/$', 'contact_info', name='contact_info'),
    #privacy
    url(r'^privacy/$', 'profile_privacy', name='profile_privacy'),
    
    
    )
urlpatterns+=    url(r'^signout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'account/signin.html','next_page':'/'},
        name='signout'),
urlpatterns+=url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'account/signin.html'}, name='user_signin'),
        
 
 
 
 
 