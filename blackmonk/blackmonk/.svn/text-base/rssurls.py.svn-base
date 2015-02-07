from django.conf.urls import patterns, url
from common.rss import list_all_rss,ArticlesRss,ClassifiedsRss,EventsRss,BusinessRss,MoviesRss

urlpatterns = patterns('',
    (r'^/?$', list_all_rss),
    (r'^articles/(?P<categoryid>[-\w]+)(.xml)\/?$', ArticlesRss()),
    (r'^classifieds/(?P<categoryid>[-\w]+)(.xml)\/?$', ClassifiedsRss()),
    (r'^events/(?P<categoryid>[-\w]+)(.xml)\/?$', EventsRss()),
    (r'^business/(?P<categoryid>[-\w]+)(.xml)\/?$', BusinessRss()),
    (r'^movies/(?P<categoryid>[-\w]+)(.xml)\/?$', MoviesRss()),
    
)
