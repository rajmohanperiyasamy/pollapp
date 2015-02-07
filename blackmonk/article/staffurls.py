from django.conf.urls import *

urlpatterns = patterns('article.staffviews',
    
    url(r'^/?$', 'list_articles', name="staff_article_home"),
    
    url(r'^ajax-listArticles/$', 'ajax_list_articles', name="staff_article_ajax_list_articles"),
    url(r'^ajax-articleState/$', 'ajax_article_state', name="staff_article_ajax_state"),
    url(r'^ajax-action/?$','ajax_article_action',name='staff_article_ajax_action'),
    
    url(r'^type/$', 'article_type', name="staff_article_select_type"),
    url(r'^add/$', 'add_article', name="staff_article_add_article"),
    
    url(r'^ajaxuploadphotos/$', 'ajax_upload_photos' ,name='staff_article_ajax_upload_photos'),
    url(r'^defaultphotos/$', 'ajax_get_default_photos' ,name='staff_article_ajax_get_default_photos'),
    url(r'^ajaxdeletephoto/(?P<pk>\d+)$', 'ajax_delete_photos', name="staffarticle_delete_photos"),
    url(r'^uploadimageyui/$', 'upload_image_from_editor',name='staff_article_upload_from_editor'),
    
    url(r'^seo/(?P<id>\d+)/$','seo',name='staff_article_seo'), 
    url(r'^changestatus/$', 'change_status', name='staff_article_change_status'),
    
    url(r'^ajax-feature-lightbox/$', 'feature_article_lightbox', name='staff_article_feature_article_lightbox'),
    url(r'^ajax-featured-image/$', 'feature_article_image', name='staff_article_feature_article_image'),
    url(r'^ajax-feature/$', 'feature_article', name='staff_article_feature_article'),
    url(r'^ajax-chkfeaturecount/$', 'feature_count', name='staff_article_feature_count'),
    
    
    url(r'^preview/(?P<id>\d+)/?$', 'article_preview',name="staff_article_preview"),
    
    #IMPORT/EXPORT
    url(r'export-csv/?$','articles_export_csv',name="staff_articles_export_csv"),
    url(r'import-csv/?$','articles_import_csv',name="staff_articles_import_csv"),
   )
 