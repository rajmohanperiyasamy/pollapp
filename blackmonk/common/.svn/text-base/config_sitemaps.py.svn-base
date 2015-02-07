import datetime

from django.contrib.sites.models import get_current_site
from django.http import HttpResponse
from django.core import urlresolvers
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.contrib.sitemaps import Sitemap
#from django.conf import settings as my_settings
from django.contrib.sitemaps.views import index as root_index,sitemap as root_sitemap
from common.models import AvailableApps
from common.utils import get_global_settings

from community.models import Entry
from community.models import Topic
from article.models import Article,ArticleCategory
from attraction.models import Attraction,AttractionCategory
from business.models import Business,BusinessCategory
from classifieds.models import Classifieds,ClassifiedCategory
from deal.models import Deal
#from forum.models import Category as DiscussionCategory,Forum as DiscussionForum ,Topic as DiscussionTopic
from events.models import Event,EventCategory
from movies.models import Movies,Theatres
from gallery.models import PhotoCategory,PhotoAlbum
from videos.models import VideoCategory,Videos

GOOGLE_NEWS_GENRE = {'FR':'UserGenerated','PR':'PressRelease, UserGenerated','RR':'Opinion','A':'UserGenerated'}#Own Story=FR, Pressrelease=PR , Advertorial=A , Review Request=RR

item_changefreq='never'
cat_changefreq='daily'
item_priority=0.5
cat_priority=0.7

def get_date():
    return datetime.date.today()

class AdvicecategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return Topic.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()

class AdviceSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Entry.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()

class ArticlecategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return ArticleCategory.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()
 
class ArticleSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Article.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()           

class AttractioncategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return AttractionCategory.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()

class AttractionSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Attraction.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()
 
class BusinesscategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return BusinessCategory.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()
  
class BusinessSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Business.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()  
    
class ClassifiedcategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return ClassifiedCategory.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()    
  
class ClassifiedSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Classifieds.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()  
  
class DealSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Deal.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()  
    
# class DiscussionCategorySitemap(Sitemap):
#     changefreq = cat_changefreq
#     priority = cat_priority
#     def items(self):
#         return DiscussionCategory.objects.all()
#     def lastmod(self, obj):
#         return get_date()
#     def location(self,obj):
#         return obj.get_absolute_url()
# 
# class DiscussionTopicSitemap(Sitemap):
#     changefreq = item_changefreq
#     priority = item_priority
#     def items(self):
#         return DiscussionForum.objects.all()
#     def lastmod(self, obj):
#         return obj.created_on
#     def location(self,obj):
#         return obj.get_absolute_url()
# 
# class DiscussionSitemap(Sitemap):
#     changefreq = item_changefreq
#     priority = item_priority
#     def items(self):
#         return DiscussionTopic.objects.filter(closed=False)
#     def lastmod(self, obj):
#         return obj.updated
#     def location(self,obj):
#         return obj.get_absolute_url()

class EventCategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return EventCategory.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()
 
class EventSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Event.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()

class TheatresSitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return Theatres.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()
 
class MoviesSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Movies.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()

class PhotoCategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return PhotoCategory.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()
 
class PhotoAlbumSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return PhotoAlbum.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()

class VideoCategorySitemap(Sitemap):
    changefreq = cat_changefreq
    priority = cat_priority
    def items(self):
        return VideoCategory.objects.all()
    def lastmod(self, obj):
        return get_date()
    def location(self,obj):
        return obj.get_absolute_url()
 
class VideoSitemap(Sitemap):
    changefreq = item_changefreq
    priority = item_priority
    def items(self):
        return Videos.objects.filter(status='P')
    def lastmod(self, obj):
        return obj.created_on
    def location(self,obj):
        return obj.get_absolute_url()
    
               
def get_available_site_map():
    apps=AvailableApps.objects.filter(sitemap='A',status='A').order_by('name')
    apps_slug=[app.slug for app in apps]
    site_map={}

    if 'advice' in apps_slug:
        site_map['advice-category']=AdvicecategorySitemap 
        site_map['advice']=AdviceSitemap 
    
    if 'articles' in apps_slug:
        site_map['article-category']=ArticlecategorySitemap 
        site_map['articles']=ArticleSitemap 
    
    if 'attractions' in apps_slug:
        site_map['attraction-category']=AttractioncategorySitemap 
        site_map['attractions']=AttractionSitemap 
    
    if 'business' in apps_slug:
        site_map['business-category']=BusinesscategorySitemap 
        site_map['business']=BusinessSitemap 
    
    if 'classifieds' in apps_slug:
        site_map['classified-category']=ClassifiedcategorySitemap 
        site_map['classifieds']=ClassifiedSitemap 
        
    if 'deals' in apps_slug:
        site_map['deals']=DealSitemap 
    
    '''if 'discussions' in apps_slug:
        site_map['discussion-category']=DiscussionCategorySitemap
        site_map['discussions-topic']=DiscussionTopicSitemap
        site_map['discussion']=DiscussionSitemap'''

    if 'events' in apps_slug:
        site_map['event-category']=EventCategorySitemap
        site_map['events']=EventSitemap 
    
    if 'movies' in apps_slug:
        site_map['movie-theatres']=TheatresSitemap
        site_map['movies']=MoviesSitemap 
    
    if 'photos' in apps_slug:
        site_map['photo-category']=PhotoCategorySitemap
        site_map['photos']=PhotoAlbumSitemap 
    
    if 'videos' in apps_slug:
        site_map['video-category']=VideoCategorySitemap
        site_map['videos']=VideoSitemap 
    
    return site_map

def index(request):
    sitemaps=get_available_site_map()
    return root_index(request,sitemaps,sitemap_url_name='common.config_sitemaps.sitemap')

def sitemap(request,section=None):
    sitemaps=get_available_site_map()
    return root_sitemap(request,sitemaps,section)

def google_news_sitemap(request):
    ''' Used for creating google news sitemap xml for articles'''
    global_settings = get_global_settings()
    articles = Article.objects.filter(status='P').order_by('-published_on')[:10]
    response = HttpResponse(mimetype='text/xml')
    data='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:n="http://www.google.com/schemas/sitemap-news/0.9">'
    for article in articles:
        tagf = ""
        data+=" <url><loc>"+global_settings.website_url+article.get_absolute_url()+"</loc>"
        data+="<n:news> <n:publication><n:name>"+global_settings.domain+"</n:name><n:language>en</n:language></n:publication>"
        try:
            genre = GOOGLE_NEWS_GENRE[article.article_type]
        except:
            genre = GOOGLE_NEWS_GENRE['FR']    
        data+="<n:genres>"+genre+"</n:genres>"
        if article.published_on:
            data+="<n:publication_date>"+str(article.published_on.strftime("%Y-%m-%d"))+"</n:publication_date>"
        else:
            data+="<n:publication_date>"+str(article.created_on.strftime("%Y-%m-%d"))+"</n:publication_date>"
        for tags in article.gettags():
            tagf= tagf + tags.tag.replace('&', '')+", "
        tagf=tagf.rstrip(', ')
        data+="<n:title>"+article.title.replace('&', 'and')+"</n:title>"
        data+="<n:keywords>"+tagf+"</n:keywords>"
        data+="</n:news></url>"
    data+="</urlset>"
    response.write(data)
    return response
