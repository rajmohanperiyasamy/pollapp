from django.conf.urls import patterns, url

urlpatterns = patterns('article.adminviews',
    url(r'^/?$', 'articles_settings', name='admin_portal_articles'),
    url(r'^settings/?$', 'articles_settings', name='admin_portal_articles_approval'),

    url(r'^category/?$', 'articles_category', name='admin_portal_articles_category'),
    url(r'^updatecategory/?$', 'articles_category_update', name='admin_portal_articles_category_update'),
    url(r'^deletecategory/?$', 'articles_category_delete', name='admin_portal_articles_category_delete'),
    url(r'^category-update-seo/?$', 'articles_seo_category_update', name='admin_portal_articles_seo_category_update'),
   
    url(r'^pricing/$', 'articles_price', name='admin_portal_articles_price'),
)