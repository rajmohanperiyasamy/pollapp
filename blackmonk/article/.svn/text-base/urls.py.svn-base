from django.conf.urls import *

urlpatterns = patterns('article.views',
    
    
    url(r'^/?$', 'list_articles', name="article_list"),
    url(r'^article-search/?$', 'search_article', name='articles_search_article'),
    
    url(r'^ajaxtellafriend/?$', 'ajax_tell_a_friend', name='article_ajax_tell_friend'),
    
    url(r'^autosuggesttag/?$', 'auto_suggest_tag',name='article_auto_suggest_tag'),
    url(r'^add_to_fav/?$', 'article_add_to_fav',name="article_add_to_fav"),  
    
    url(r'^(?P<catslug>[-\w]+)/$', 'article_category_list', name="article_category_list"),
    
    url(r'^(?P<my>\d{3,4})/(?P<slug>[-\w]+)(.html)\/?$', 'article_details', name="article_details"),
    url(r'^pdf/(?P<id>\d+)/(?P<pdf>\d+)/?$', 'article_details_print_pdf',name="article_details_pdf"),
    url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'article_details'),
    
           )
