from django.conf.urls import *
urlpatterns = patterns('common.designviews',
    
    #CONFIGURATION 
    url(r'^/?$', 'design_overview', name='admin_design_overview'),
    url(r'^navigation/?$', 'manage_navigation', name='admin_design_manage_navigation'),
    
    #Header Menu Configurations
    url(r'^update-menu-positions/?$', 'update_menu_positions', name='admin_design_update_menu_positions'),
    url(r'^reset-menu-positions/?$', 'reset_menu_positions', name='admin_design_reset_menu_positions'),
    url(r'^update-menu-item/?$', 'update_menu_item', name='admin_design_update_menu_item'),
    url(r'^delete-menu-item/?$', 'delete_menu_item', name='admin_design_delete_menu_item'),
    
    #Sub Header Menu Configurations
    url(r'^subnavigation/?$', 'manage_subheader_navigation', name='admin_design_manage_subheader_navigation'),
    url(r'^update-subheader-item/?$', 'update_subheader_item', name='admin_design_update_subheader_item'),
    url(r'^update-subheader-positions/?$', 'update_subheader_positions', name='admin_design_update_subheader_positions'),
    
    #Copyright Settings
    url(r'^copyright/?$', 'manage_copyright', name='admin_design_manage_copyright'),
    url(r'^update-copyright/?$', 'update_copyright_info', name='admin_design_update_copyright_info'),
    
    #Footer Menu Configuration
    url(r'^footer/?$', 'manage_footer', name='admin_design_manage_footer'),
    url(r'^update-footer-item/?$', 'update_footer_item', name='admin_design_update_footer_item'),
    url(r'^update-footer-positions/?$', 'update_footer_positions', name='admin_design_update_footer_positions'),
)