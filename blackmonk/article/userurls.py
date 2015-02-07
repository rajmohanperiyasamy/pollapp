from django.conf.urls import *

urlpatterns = patterns('article.userviews',
                       
                       
    url(r'^/?$', 'dash_board',name="article_dash_board"),  
     
    url(r'^ajax-listArticles/$', 'ajax_dash_board', name="article_ajax_dash_board"),
    url(r'^ajax-articleState/$', 'ajax_article_state', name="article_ajax_state"),
    url(r'^ajax-action/?$','ajax_article_action',name='article_ajax_action'), 
    
    
    url(r'^type/$', 'article_type', name="article_select_type"),
    url(r'^add/$', 'add_article', name="article_add_article"),
    
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='article_ajax_upload_photos'),
    url(r'^defaultphotos/$', 'ajax_get_default_photos' ,name='article_ajax_get_default_photos'),
    url(r'^uploadimageyui/$', 'upload_image_from_editor',name='article_upload_from_editor'),
                     
    url(r'^preview/(?P<id>\d+)/?$', 'article_user_preview',name="user_article_preview"),
    url(r'^seo/(?P<id>\d+)/$','seo',name='article_update_seo'),   
                       
    )                 