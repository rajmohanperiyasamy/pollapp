#Python Libs
import datetime

#Django Libs
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist

#Module Files(models,forms etc...)
from article.models import ArticleCategory,Article
from classifieds.models import ClassifiedCategory,Classifieds
from business.models import BusinessCategory,Business
from events.models import EventCategory,Event
from movies.models import Movies
from common.utils import get_global_settings

global_settings = get_global_settings()

##New Method using Rss201rev2Feed
def list_all_rss(request):
    data={}
    data['article_categories'] = ArticleCategory.objects.all().order_by('name')
    data['classified_categories'] = ClassifiedCategory.objects.filter(parent__isnull=True).order_by('name')
    data['business_categories'] = BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('name')
    data['event_categories'] = EventCategory.objects.all().order_by('name')
    return render_to_response('default/common/rss-list.html',data,context_instance=RequestContext(request))

class ArticlesRss(Feed):
    description_template = 'feeds/city_description.html'
    def get_object(self, request, categoryid):
        if categoryid == 'all':
            return False
        else:
            catobj = ArticleCategory.objects.get(id = categoryid)
            return catobj
    # set the category values
    def title(self, obj):
        if obj:
            return obj.name
        else:
            return _('Latest Article')
    def link(self, obj):
        if obj:
            return obj.get_absolute_url()
        else:
            return global_settings.website_url
    #  set the one by one objects
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.summary
    def items(self, obj):
        if obj:
            return Article.objects.filter(category = obj,status='P').order_by('-id')[:15]
        else:
            return Article.objects.filter(status='P').order_by('-id')[:50]

class ClassifiedsRss(Feed):
    description_template = 'feeds/city_description.html'
    def get_object(self, request, categoryid):
        if categoryid == 'all':
            return False
        else:
            catobj = ClassifiedCategory.objects.get(id = categoryid)
            return catobj
    # set the category values
    def title(self, obj):
        if obj:
            return obj.name
        else:
            return _('Latest Classifieds')    
    def link(self, obj):
        if obj:
            return obj.get_absolute_url()
        else:
            return global_settings.website_url
    #  set the one by one objects
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        try:return item.description.encode('utf-8')[:100]
        except:pass
    def items(self, obj):
        if obj:
            return Classifieds.objects.filter(category__parent = obj,status='P').distinct().order_by('-id')[:15]
        else:
            return Classifieds.objects.filter(status='P').distinct().order_by('-id')[:50]
        
class EventsRss(Feed):
    description_template = 'feeds/city_description.html'
    def get_object(self, request, categoryid):
        if categoryid == 'all':
            return False
        else:
            catobj = EventCategory.objects.get(id = categoryid)
            return catobj
    # set the category values
    def title(self, obj):
        if obj:
            return obj.name
        else:
            return _('Latest Events')
    def link(self, obj):
        if obj:
            return obj.get_absolute_url()
        else:
            return global_settings.website_url
    #  set the one by one objects
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.event_description.encode('utf-8')[:100]
    def items(self, obj):
        if obj:
            return Event.objects.filter(category=obj,status='P').distinct().order_by('-id')[:15]
        else:
            return Event.objects.filter(status='P').distinct().order_by('-id')[:50]

class BusinessRss(Feed):
    description_template = 'feeds/city_description.html'
    def get_object(self, request, categoryid):
        if categoryid == 'all':
            return False
        else:
            catobj = BusinessCategory.objects.get(id = categoryid)
            return catobj
    # set the category values
    def title(self, obj):
        if obj:
            return obj.name
        else:
            return _('Latest Business')
    def link(self, obj):
        if obj:
            return obj.get_absolute_url()
        else:
            return global_settings.website_url
    #  set the one by one objects
    def item_title(self, item):
        return item.name
    def item_description(self, item):
        try:return item.description.encode('utf-8')[:100]
        except:pass
    def items(self, obj):
        if obj:
            return Business.objects.filter(categories__parent_cat=obj,status='P').distinct().order_by('-id')[:15]
        else:
            return Business.objects.filter(status='P').distinct().order_by('-id')[:50]
 
class MoviesRss(Feed):
    description_template = 'feeds/city_description.html'
    # set the category values
    def title(self, obj):
        if obj:
            return obj.name
        else:
            return _('Latest Movies')
    def link(self, obj):
        if obj:
            return obj.get_absolute_url()
        else:
            return global_settings.website_url
    #  set the one by one objects
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        try:return item.synopsis.encode('utf-8')[:100]
        except:pass
    def items(self, obj):
        return Movies.objects.filter(status='P').order_by('-id')[:50]
    