# Python Libs 
import datetime 
import math

# Django Libs 
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils import simplejson
from channels.models import Channel
#Module Files(models,forms etc...)
from banners.models import BannerZones, BannerAdvertisements, BannerSections, BannerReports

def _get_category_model(module):
    from community.models import Topic
    from bookmarks.models import BookmarkCategory
    from business.models import BusinessCategory
    from article.models import ArticleCategory
    from events.models import EventCategory
    from videos.models import VideoCategory
    from gallery.models import PhotoCategory
    from attraction.models import AttractionCategory
    from deal.models import DealCategory
    from classifieds.models import ClassifiedCategory
    from channels.models import Channel
    
    CATEGORY_MODELS = {'community':Topic, 'bookmarks':BookmarkCategory, 'business':BusinessCategory, 
                       'articles':ArticleCategory, 'deals':DealCategory, 'events':EventCategory, 
                       'attractions':AttractionCategory,'channels':Channel, 'photos':PhotoCategory, 'videos':VideoCategory, 'classifieds':ClassifiedCategory }
    try:cat_model = CATEGORY_MODELS[module]
    except:cat_model = False
    return cat_model 

def get_banner_ads(request):
    ''' method for displaying banner ads for each module '''
    from django.contrib.contenttypes.models import ContentType
    global_banner_name = 'global-banner'
    
    right_template = 'default/banners/right-side-banners.html'
    channel_module = 'channels'
    try:module = request.GET['url'].split('/')[3]
    except:module = global_banner_name
    try:
        channel = Channel.objects.get(slug = module)
        if channel:
            module = channel_module
    except:module =module
    if module == '':module = 'home'
    try:
        try:section = BannerSections.objects.get(slug = module)
        except:section = BannerSections.objects.get(slug = global_banner_name)
        try:
            try:category = _get_category_model(module).objects.get(slug = request.GET['url'].split('/')[4])
            except:
                try:category = _get_category_model(module).objects.get(slug = request.GET['url'].split('/')[3])
                except:category = None    
            content_type = ContentType.objects.get_for_model(category)
            right_banners = BannerAdvertisements.objects.filter(section=section, zones__slot='R', content_type=content_type, object_id = category.id, status = 'P').order_by('?')[:1]
        except:
            right_banners = BannerAdvertisements.objects.filter(section=section, zones__slot='R', status = 'P').exclude(object_id__isnull = False).order_by('?')[:1]
        
        if not right_banners:
            right_banners = BannerAdvertisements.objects.filter(section=section, zones__slot='R', status = 'P').exclude(object_id__isnull = False).order_by('?')[:1]
        if right_banners.count() == 0:right_banners = BannerAdvertisements.objects.filter(section__slug = global_banner_name, zones__slot='R', status = 'P').order_by('?')[:1]
        if not right_banners.count() == 0:
            right_banner_html = render_to_string(right_template,{'banners':right_banners})
        else:
            right_banner_html = ""
        data={'right_banner_html':right_banner_html}
    except:
        data={'right':False,'top':False}
    return HttpResponse(simplejson.dumps(data))     

def get_banner_ads_top(request):
    ''' method for displaying top banner ads for each module '''
    from django.contrib.contenttypes.models import ContentType
    global_banner_name = 'global-banner'
    
    top_template = 'default/banners/top-banners.html'
    
    try:module = request.GET['url'].split('/')[3]
    except:module = global_banner_name
    if module == '':module = 'home'
    
    try:
        try:section = BannerSections.objects.get(slug = module)
        except:section = BannerSections.objects.get(slug = global_banner_name)
        try:
            try:category = _get_category_model(module).objects.get(slug = request.GET['url'].split('/')[4])
            except:category = None    
            content_type = ContentType.objects.get_for_model(category)
            top_banners =  BannerAdvertisements.objects.filter(section=section,zones__slot='T', content_type=content_type, object_id = category.id, status = 'P').order_by('?')[:1]
        except:
            top_banners =  BannerAdvertisements.objects.filter(section=section, zones__slot='T', status = 'P').exclude(object_id__isnull = False).order_by('?')[:1]
        
        if not top_banners:
            top_banners = BannerAdvertisements.objects.filter(section=section, zones__slot='T', status = 'P').exclude(object_id__isnull = False).order_by('?')[:1]
            
        if top_banners.count() == 0:top_banners =  BannerAdvertisements.objects.filter(section__slug = global_banner_name, zones__slot='T', status = 'P').order_by('?')[:1]
            
        top_banner_html = render_to_string(top_template,{'banners':top_banners})
        data={'top_banner_html':top_banner_html}
    except:
        data={'right':False,'top':False}
    
    return HttpResponse(simplejson.dumps(data))  


def get_banner_ads_bottom(request):
    ''' method for displaying bottom banner ads for each module '''
    from django.contrib.contenttypes.models import ContentType
    global_banner_name = 'global-banner'
    
    bottom_template = 'default/banners/bottom-banners.html'
    
    try:module = request.GET['url'].split('/')[3]
    except:module = global_banner_name
    if module == '':module = 'home'
    
    try:
        try:section = BannerSections.objects.get(slug = module)
        except:section = BannerSections.objects.get(slug = global_banner_name)
        try:
            try:category = _get_category_model(module).objects.get(slug = request.GET['url'].split('/')[4])
            except:category = None    
            content_type = ContentType.objects.get_for_model(category)
            bottom_banners =  BannerAdvertisements.objects.filter(section=section,zones__slot='B', content_type=content_type, object_id = category.id, status = 'P').order_by('?')[:1]
        except:
            bottom_banners =  BannerAdvertisements.objects.filter(section=section, zones__slot='B', status = 'P').exclude(object_id__isnull = False).order_by('?')[:1]
        
        if not bottom_banners:
            bottom_banners = BannerAdvertisements.objects.filter(section=section, zones__slot='B', status = 'P').exclude(object_id__isnull = False).order_by('?')[:1]
            
        if bottom_banners.count() == 0:bottom_banners =  BannerAdvertisements.objects.filter(section__slug = global_banner_name, zones__slot='B', status = 'P').order_by('?')[:1]
            
        bottom_banner_html = render_to_string(bottom_template,{'banners':bottom_banners})
        data={'bottom_banner_html':bottom_banner_html}
    except:
        data={'right':False,'top':False}
    
    return HttpResponse(simplejson.dumps(data))  



def update_banner_views(request):
    ''' ajax method for update banner views'''
    bannerids = request.GET.get('bannerids',False)
    try:
        if bannerids:
            try:bannerids = bannerids.split(',')
            except:bannerids = bannerids
            banners = BannerAdvertisements.objects.filter(id__in=bannerids)
            for banner in banners:
                br_obj = BannerReports(banner=banner)
                br_obj.views = br_obj.views + 1
                br_obj.viewed_on = datetime.datetime.now()
                try:br_obj.ipaddress = request.META['REMOTE_ADDR']
                except:pass 
                try:br_obj.source_url = request.META['HTTP_REFERER']
                except:pass 
                br_obj.save() 
        return HttpResponse('1')        
    except:return HttpResponse('0')        
            
def update_banner_clicks(request):
    ''' ajax method to update banner clicks'''
    try:
        banner = BannerAdvertisements.objects.get(id = request.GET['bid'])
        br_obj = BannerReports(banner=banner)
        br_obj.clicks = br_obj.clicks + 1
        br_obj.is_clicked = True
        br_obj.viewed_on = datetime.datetime.now()
        try:br_obj.ipaddress = request.META['REMOTE_ADDR']
        except:pass 
        try:br_obj.source_url = request.META['HTTP_REFERER']
        except:pass 
        br_obj.save() 
        return HttpResponse('1')        
    except:return HttpResponse('0')   
    
