from django.conf.urls import *

urlpatterns = patterns('community.views',
    url(r'^/?$', 'community_listing', name="community_listing"),
    url(r'^(?P<type>[-\w]+)/?$', 'community_listing', name="community_listing"),
    url(r'^(?P<top>[-\w]+)/(?P<slug>[-\w]+)(.html)\/?$', 'entry_detail', name="community_entry_details"),
    url(r'^entry/add_entry/?$', 'add_entry', name="add_entry"),
    
    url(r'^follow_entry/(?P<id>\d+)/?$', 'entry_follow',name="entry_follow"),
    url(r'^unfollow_entry/(?P<id>\d+)/?$', 'entry_unfollow',name="entry_unfollow"),
    
    url(r'^follow_topic/(?P<id>\d+)/?$', 'topic_follow',name="topic_follow"),
    url(r'^unfollow_topic/(?P<id>\d+)/?$', 'topic_unfollow',name="topic_unfollow"),
    
    url(r'^saveans/(?P<id>\d+)/?$', 'save_answer', name="question_save_answer"),
    
    url(r'^loadanscomment/(?P<objid>\d+)/?$', 'load_comment', name="answer_load_comment"),
    
     url(r'^answer-rating/ajax-answer-user-rating/?$', 'answer_user_rating', name="answer_answer_user_rating"),
    url(r'^ajax-viewed/(?P<id>\d+)/?$', 'ajax_viewed', name="entry_ajax_viewed"),
    ####comment urls###
    url(r'^comment/post/$','community_post_comment',name='community_comments_post_comment'),
    url(r'^comment/reply/$','community_replay_comment',name='community_comment_reply'),
    url(r'^comment/load_more_comment/$','community_load_more_comment',name='community_load_more_comment'),
    url(r'^comment/load_parent_comment/$','community_load_parent_comment',name='community_load_parent_comment'),
    
)
