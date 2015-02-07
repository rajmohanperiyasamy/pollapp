from django.conf.urls import patterns, url
from django.contrib.comments.urls import urlpatterns as contrib_comments_urlpatterns

urlpatterns = patterns('mptt_comments.views',
    url(r'^reply/$','replay_comment',name='comment_reply'),
    url(r'^post/$','post_comment',name='comments_post_comment'),
    url(r'^likedislike/$','like_dislike',name='comments_like_dislike'),
    url(r'^flag/$','flag',name='comments_flag'),
    
    url(r'^load_more_comment/$','load_more_comment',name='load_more_comment'),
    url(r'^load_parent_comment/$','load_parent_comment',name='load_parent_comment'),
    
    url(r'^more/(\d+)/$','comments_more', name='comments_more'),
    url(r'^replies/(\d+)/$','comments_subtree',name='comments_subtree'),
    url(r'^detail/(\d+)/$','comments_subtree',name='comment_detail', kwargs={'include_self': True, 'include_ancestors': True}),
    url(r'^load-review/(?P<object_id>\d+)/(?P<model>\w+)/$','load_review', name="load_review"),
    url(r'^check-review/(?P<object_id>\d+)/(?P<model>\w+)/$','check_review', name="check_review"),
    
    url(r'^load-comment-form/(?P<object_id>\d+)/(?P<model>\w+)/$','load_comment_form', name="load_comment_form"),
    url(r'^load-initial-comments/(?P<object_id>\d+)/(?P<model>\w+)/(?P<appname>\w+)/$','get_initial_mptt_comment_list', name="get_initial_mptt_comment_list"),
)

urlpatterns += contrib_comments_urlpatterns
