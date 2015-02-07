from django.conf.urls import patterns, url

urlpatterns = patterns('news.adminviews',
    url(r'^/?$', 'news_settings', name='admin_portal_news'),
    url(r'^settings/?$', 'news_settings', name='admin_portal_news_settings'),
    
    url(r'^category/?$', 'news_category', name='admin_portal_news_category'),
    url(r'^updatecategory/?$', 'news_category_update', name='admin_portal_news_category_update'),
    url(r'^deletecategory/?$', 'news_category_delete', name='admin_portal_news_category_delete'),
    url(r'^seocategoryupdate/?$', 'news_seo_category_update', name='admin_portal_news_seo_category_update'),
    
    url(r'^provider/?$', 'news_provider', name='admin_portal_news_provider'),
    url(r'^updateprovider/?$', 'news_provider_update', name='admin_portal_news_provider_update'),
    url(r'^deleteprovider/?$', 'news_provider_delete', name='admin_portal_news_provider_delete'),
    url(r'^changestatusprovider/?$', 'news_provider_change_status', name='admin_portal_news_provider_change_status'),
    url(r'^ajax-update-news/?$', 'update_news', name='admin_portal_update_news'),
)