from django.conf.urls import patterns, include, url
from article.views import HelloTemplate
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

#if settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT}))
#    
urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'article.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', 'article.views.hello',name='hello'),
    url(r'^hello_template/$','article.views.hello_template'),
    url(r'^test$', 'article.views.Test', name='test'),  
    url(r'^add_author/$','article.views.add_author', name='add_author'),
    url(r'^edit_author/(?P<pk>\d+)/$', 'article.views.add_author', name='update_author'),
    url(r'^add_article/$','article.views.add_article', name='add_article'),
    url(r'hello_classview/$', HelloTemplate.as_view()),    
    url(r'add_author/$','article.views.add_author', name='add_author'),
    url(r'contact/$','article.views.contact', name='contact'),
    url(r'calculate/$','article.views.calculate', name='calculate'),
    url(r'clients_data/(?P<pk>\d+)$','article.views.clients_data', name='clients_data'),
    url(r'report/$','article.views.report', name='report'),
    url(r'date/$','article.views.date', name='date'),
    url(r'bsoup/$','article.views.fetch_images', name='fetch_images'),
    url(r'fetch/$','article.views.fetch', name='fetch'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^download/(?P<pk>\d+)$', 'article.views.download',name='download'),
    url(r'^list/$', 'article.views.list', name='list'),
    
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
