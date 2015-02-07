from django.conf.urls import *
urlpatterns = patterns('usermgmt.adminviews',

    #  USERS MANAGEMENT  #   
    url(r'^/?$', 'admin_overviews', name='admin_portal_usermanagement'),
    url(r'^users/?$', 'display_users', name='admin_display_users'),
    url(r'^ajax-display-users/$', 'ajax_display_users', name='admin_ajax_display_users'),
    url(r'^ajax-change-user-status/$', 'ajax_change_user_status', name='admin_ajax_change_user_status'),
    url(r'^ajax-deactivate-user-status/$', 'ajax_deactivate_user_status', name='admin_ajax_deactivate_user_status'),
    url(r'^ajax-create-user/$', 'ajax_create_user', name='admin_ajax_create_user'),
    url(r'^ajax-update-user/$', 'ajax_update_user', name='admin_ajax_update_user'),
    url(r'^ajax-delete-user/$', 'ajax_delete_user', name='admin_ajax_delete_user'),
    url(r'^ajax-delete-deactivate-user/(?P<id>\d+)/$', 'ajax_delete_type', name='admin_ajax_delete_type'),
    url(r'^ajax-promote-user/(?P<id>\d+)/$', 'ajax_promote_user', name='admin_ajax_promote_user'),
    url(r'^ajax-user-stats/$', 'get_user_stats', name='admin_ajax_get_user_stats'),
    url(r'^ajax-user-actions/$', 'ajax_users_action', name='admin_ajax_users_action'),
    url(r'^ajax-user-profile/$', 'ajax_user_profile', name='admin_ajax_user_profile'),
    url(r'^ajax-user-contribution/$', 'get_user_contribution', name='admin_ajax_get_user_contribution'),
    url(r'^importcsv/$', 'import_users_csv', name='admin_import_users_csv'),
    url(r'^exportcsv/$', 'export_users_to_csv', name='admin_export_users_to_csv'),
    
    #  STAFF MANAGEMENT #   
    url(r'^staffs/$', 'display_staff', name='admin_display_staff'),
    url(r'^ajax-display-staffs/$', 'ajax_display_staff', name='admin_ajax_display_staff'),
    url(r'^ajax-update-staff-roll/$', 'ajax_update_staff_roll', name='admin_ajax_update_staff_roll'),
    url(r'^ajax-create-staff/$', 'ajax_create_staff', name='admin_ajax_create_staff'),
    url(r'^ajax-update-staff/$', 'ajax_update_staff', name='admin_ajax_update_staff'),
    url(r'^ajax-update-staff-rolls-count/$', 'ajax_update_staff_rolls_count', name='admin_ajax_update_staff_rolls_count'),
    url(r'^ajax-delete-staff/$', 'ajax_delete_staff', name='admin_ajax_delete_staff'),
    url(r'^ajax-staff-actions/$', 'ajax_staff_action', name='admin_ajax_staff_action'),
    
    #  ROLE MANAGEMENT #   
    url(r'^addrole/$', 'add_role', name='admin_add_role'),
    url(r'^deleterole/$', 'delete_role', name='admin_delete_role'),

)