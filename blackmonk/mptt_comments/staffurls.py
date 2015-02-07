from django.conf.urls import patterns, url

urlpatterns = patterns('mptt_comments.staffviews',
    url(r'^/?$', 'comments',name="staff_comments"),
    url(r'^(?P<model>[-\w]+)/?$', 'comments',name="staff_comments_model"),
    url(r'^a/ajax/?$', 'ajax_comments',name="staff_ajax_comments"),
    url(r'^a/ajax/(?P<model>[-\w]+)/?$', 'ajax_comments',name="staff_ajax_comments_model"),
    url(r'^a/action/?$', 'ajax_comment_action',name="staff_ajax_comment_action"),
    url(r'^a/action/(?P<model>[-\w]+)/?$', 'ajax_comment_action',name="staff_ajax_comment_action_model"),
    url(r'^a/change-status/?$', 'comment_status_change',name="staff_comment_status_change"),
    
    #url(r'^a/action-community/(?P<model>[-\w]+)/?$', 'ajax_community_comment_action',name="staff_ajax_community_comments"),
    #url(r'^a/community-change-status/?$', 'community_comment_status_change',name="staff_community_comment_status_change"),
    #url(r'^/?$', 'comments_all',name="staff_comments_all"),
    #url(r'^(?P<model>[-\w]+)/(?P<object_pk>\d+)/?$', 'comment_list',name="staff_comments_listing"),           
 )