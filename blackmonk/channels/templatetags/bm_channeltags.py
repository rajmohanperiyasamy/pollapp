import datetime
from datetime import date

from django.core.cache import cache
from django.template import Library
from channels.models import Channel
from business.models import Business,BusinessCategory, BusinessCoupons
from article.models import Article
from deal.models import Deal
from movies.models import Movies
from attraction.models import Attraction
from common.views import __getpoll
from gallery.models import PhotoAlbum 
from videos.models import Videos
from mptt_comments.models import MpttComment
from common.utils import ds_sortby_listingtype
register = Library()

@register.assignment_tag
def show_featured_business(**kwargs):
    limit = kwargs.get('limit',12)
    channel = kwargs.get('channel',False)
    if cache.get('featuredbusiness'+str(channel.slug)):
        featuredbusiness = cache.get('featuredbusiness'+str(channel.slug))
        return featuredbusiness
    else:
        featuredbusiness = Business.objects.filter(status='P',featured_sponsored='F', categories__in=channel.businesswidget.categories.all()).only('name','logo','slug','ratings').prefetch_related('categories','address').select_related('logo').order_by('-id').distinct()[:limit]
        if featuredbusiness.count() < 5:
            featuredbusiness = ds_sortby_listingtype(Business).filter(status='P',lend_date__gte=date.today(),categories__in=channel.businesswidget.categories.all()).only('name','logo','slug','album','categories','address').prefetch_related('categories','address').select_related('logo','album').order_by('-created_on')[:5]
        cache.set('featuredbusiness'+str(channel.slug), featuredbusiness, 900) 
        return featuredbusiness

@register.assignment_tag
def get_featured_article(**kwargs):
    limit = kwargs.get('limit',12)
    channel = kwargs.get('channel',False)
    if cache.get('articles'+str(channel.slug)):
        articles = cache.get('articles'+str(channel.slug))
        return articles
    else:
        try:
            featured_article = Article.objects.filter(status = 'P', featured=True, category__in=channel.articlewidget.categories.all()).only('title','slug','category','summary','created_on','album','published_on','created_by').select_related('category','created_by').prefetch_related('album').distinct().order_by('-id')
            main_article = featured_article[0]
            sub_article = featured_article[1:3]
        except:
            main_article = False
            sub_article = False
        articles = {'main_article':main_article, 'sub_article':sub_article}
        cache.set('articles'+str(channel.slug), articles, 900)
        return {'main_article':main_article, 'sub_article':sub_article}

@register.assignment_tag
def show_latest_business(**kwargs):
    limit = kwargs.get('limit',12)
    channel = kwargs.get('channel',False)
    if cache.get('latest_business_category'+str(channel.slug)):
        latest_business_category = cache.get('latest_business_category'+str(channel.slug))
        return latest_business_category
    else:
        try:
            business_categories = channel.businesswidget.categories.all()
            latest_business = Business.objects.filter(status='P',categories__in=channel.businesswidget.categories.all()).only('name','logo','slug','ratings').prefetch_related('categories','address').select_related('logo').order_by('-id').distinct()[:limit]
        except:
            latest_business = False
            business_categories = False
        latest_business_category = {'latest_business':latest_business,'business_categories':business_categories}
        cache.set('latest_business_category'+str(channel.slug), latest_business_category, 900)
        return {'latest_business':latest_business,'business_categories':business_categories}

@register.assignment_tag
def get_home_page_featured_deals(**kwargs):
    limit = kwargs.get('limit',1)
    channel = kwargs.get('channel',False)
    fetched_values = ['title','slug','about','original_price','discount_price','end_date','album', 'max_count']
    try:
        today = date.today()
        featured_deals =  Deal.objects.only(*fetched_values).filter(status='P',featured = True, end_date__gte=today, start_date__lte=today,category__in=channel.dealwidget.categories.all()).select_related('album').order_by('-created_on')[:limit]
    except:
        featured_deals = False
    return featured_deals

@register.assignment_tag
def get_home_page_business_offers(**kwargs):
    limit = kwargs.get('limit',3)
    channel = kwargs.get('channel',False)
    try:
        offers = BusinessCoupons.objects.filter(business__status='P',end_date__gte=date.today(),business__categories__in=channel.businesswidget.categories.all()).only('title','business','photo').select_related('business').order_by('-id').distinct()[:limit]
    except:
        offers = False
    return offers

@register.assignment_tag
def get_attraction_categories(**kwargs):
    limit = kwargs.get('limit',1)
    channel = kwargs.get('channel',False)
    try:
        attract_categories = channel.attractionwidget.categories.all()
        attraction = Attraction.objects.filter(category__in = attract_categories, status = 'P').only('name','venue').select_related('venue').order_by('-id').distinct()
    except:
        attract_categories = False
        attraction = False
    return {'attract_categories':attract_categories,'attraction':attraction}

@register.assignment_tag
def get_channel_page_movies(**kwargs):
    limit = kwargs.get('limit',4)
    today = datetime.datetime.now()
    fetched_values = ['title','slug','image','release_date','certification']
    try:
        movies_pack = {}
        movies_pack['released_movies'] = Movies.objects.only(*fetched_values).filter(release_date__lte=today, status='P').order_by('-release_date')[:15]
        movies_pack['datelist'] = [ today + datetime.timedelta(days=x) for x in range(0,7) ]
    except:
        movies_pack = False
    return movies_pack

@register.assignment_tag
def get_channel_poll(**kwargs):
    request = kwargs.get('request',False)
    try:
        polldata = __getpoll(request)
    except:
        polldata = False
    return polldata

@register.assignment_tag
def get_featured_albums_and_videos(**kwargs):
    limit = kwargs.get('limit',1)
    channel = kwargs.get('channel',False)
    if cache.get('gallery'+str(channel.slug)):
        featured_gallery_pack = cache.get('gallery'+str(channel.slug))
        return featured_gallery_pack
    else:
        try:
            featured_gallery_pack = {}
            featured_gallery_pack['main_featured_video'] = main_featured_video = Videos.objects.only("title","slug","video_id").filter(status='P',featured=True,category__in=channel.videowidget.categories.all()).order_by('-id')[:1]
            featured_gallery_pack['featured_albums'] = PhotoAlbum.objects.filter(status='P',is_featured=True,category__in=channel.gallerywidget.categories.all()).order_by('-id')[:2]
            featured_gallery_pack['featured_videos'] =  Videos.objects.only("title","slug","video_id").filter(status='P',featured=True,category__in=channel.videowidget.categories.all()).exclude(id__in = main_featured_video).order_by('-id')[:2]
        except:
            featured_gallery_pack = False
        cache.set('gallery'+str(channel.slug), featured_gallery_pack, 900)
        return featured_gallery_pack

@register.assignment_tag
def get_recent_reviews(**kwargs):
    limit = kwargs.get('limit',4)
    channel = kwargs.get('channel',False)
    if cache.get('reviews'+str(channel.slug)):
        reviews = cache.get('reviews'+str(channel.slug))
        return reviews
    else:
        try:
            business_categories = channel.businesswidget.categories.all()
            latest_business = Business.objects.filter(status='P',categories__in=channel.businesswidget.categories.all()).values_list('id',flat=True)
            latest_business = set(latest_business)
            reviews = MpttComment.objects.filter(object_pk__in = latest_business ,content_type__model__iexact='business',level__gte=1)[:limit]
        except:
            reviews = False
        cache.set('reviews'+str(channel.slug), reviews, 900)
        return reviews



