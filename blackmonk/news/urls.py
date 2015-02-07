from django.conf.urls import *

urlpatterns = patterns('news.views',            
    url(r'^/?$','index',name='news_home'),
    url(r'^(?P<cat>[-\w]+)\/?$','index',name='news_by_category'),
    url(r'^(?P<slug>[-\w]+)(.html)\/?$','news_detail',name='news_in_detail'),
)