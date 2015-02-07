from datetime import date
from django.core.cache import cache
from django.template import Library
from business.models import Business, BusinessCoupons, BusinessProducts
from django.contrib.contenttypes.models import ContentType
from mptt_comments.models import MpttComment
from common.utils import ds_sortby_listingtype

register = Library()
CACHE_TIMEOUT = 60*10

@register.inclusion_tag('default/custom_tags.html')
def show_featured_business(template='default/sliders/featured_biz_doublerow.html'):
    featuredbusiness=cache.get('cache_featured_business')
    if featuredbusiness is None:
        featuredbusiness = Business.objects.filter(status='P',featured_sponsored='F',lend_date__gte=date.today()).only('name','logo','slug','album','categories','address').prefetch_related('categories','address').select_related('logo','album').order_by('-id')
        if featuredbusiness.count() < 6:
            featuredbusiness = ds_sortby_listingtype(Business).filter(status='P',lend_date__gte=date.today()).only('name','logo','slug','album','categories','address').prefetch_related('categories','address').select_related('logo','album').order_by('-created_on')[:6]
        cache.set('cache_featured_business',featuredbusiness,CACHE_TIMEOUT)
    return {'template': template,'businesslist':featuredbusiness,'listing_type':'fb'}

@register.inclusion_tag('default/custom_tags.html')
def show_latest_business_gallery(template='default/business/biz_gallery_aside.html'):
    latestbusiness = Business.objects.filter(status='P', is_claimable=False, created_by__is_staff=False, lend_date__gte=date.today()).exclude(album=None).select_related('album').order_by('-created_on')[:5]
    if not latestbusiness.exists():
        latestbusiness = Business.objects.filter(status='P', is_claimable=False, lend_date__gte=date.today()).exclude(album=None).select_related('album').order_by('-created_on')[:5]
    return {'template': template,'businesslist': latestbusiness}

@register.inclusion_tag('default/custom_tags.html')
def show_recent_business_review(template='default/movies/recent-reviews.html'):
    recent_reviews =[]
    try:
        c_type = ContentType.objects.get(model='business')
        recent_reviews = MpttComment.objects.filter(content_type=c_type,level__gte=1,is_public=True,is_removed=False).order_by('-submit_date')[:4]
    except:
        pass
    return {'template': template, 'recent_reviews': recent_reviews}

@register.inclusion_tag('default/custom_tags.html')
def show_recommend_business(template='default/sliders/featured_biz.html'):
    recommendedbusiness=cache.get('cache_recommendedbusiness')
    if recommendedbusiness is None:
        recommendedbusiness = Business.objects.filter(status='P',lend_date__gte=date.today()).exclude(ratings=0.0).only('name','logo','slug','album','categories','address').prefetch_related('categories','address').select_related('logo','album').order_by('-ratings')
        cache.set('cache_recommendedbusiness',recommendedbusiness,CACHE_TIMEOUT)
    return {'template': template,'businesslist':recommendedbusiness,'listing_type':'rb'}

@register.inclusion_tag('default/custom_tags.html')
def show_latest_business(template='default/sliders/featured_biz_doublerow.html'):
    latestbusiness=cache.get('cache_latestbusiness')
    if latestbusiness is None:
        latestbusiness = Business.objects.filter(status='P',lend_date__gte=date.today()).only('name','logo','slug','album','categories','address').prefetch_related('categories','address').select_related('logo','album').order_by('-created_on')[:10]
        cache.set('cache_latestbusiness',latestbusiness,CACHE_TIMEOUT)
    return {'template': template,'businesslist':latestbusiness,'listing_type':'lb'}

@register.inclusion_tag('default/business/offers-list.html')
def show_all_business_offers(**kwargs):
    limit = kwargs.get('limit', 5)
    cache_key='offers'+str(limit)
    offers=cache.get(cache_key)
    if offers is None:
        offers = BusinessCoupons.objects.filter(business__status='P',end_date__gte=date.today()).defer('is_active','created_by','created_on','type').select_related('business').order_by('-id')[:limit]
        cache.set(cache_key,offers,CACHE_TIMEOUT)
    return {'objects':offers, 'type': 'offers'}

@register.inclusion_tag('default/business/offers-list.html')
def show_all_business_product(**kwargs):
    limit = kwargs.get('limit', 5)
    cache_key='products'+str(limit)
    products=cache.get(cache_key)
    if products is None:
        products = BusinessProducts.objects.filter(business__status='P').select_related('business').order_by('-id')[:limit]
        cache.set(cache_key,products,CACHE_TIMEOUT)
    return {'objects':products, 'type': 'products'}

@register.assignment_tag
def get_home_page_featured_business(limit):
    cache_key='featuredbusiness'+str(limit)
    featuredbusiness=cache.get(cache_key)
    if featuredbusiness is None:
        featuredbusiness= Business.objects.filter(status='P',featured_sponsored='F',lend_date__gte=date.today()).only('name','logo','slug','ratings').prefetch_related('categories').select_related('logo').order_by('-id')[:limit]
        if len(featuredbusiness) < 4:
            featuredbusiness = ds_sortby_listingtype(Business).filter(status='P',lend_date__gte=date.today()).only('name','logo','slug','ratings').prefetch_related('categories').select_related('logo').order_by('-created_on')[:4]
        cache.set(cache_key,featuredbusiness,CACHE_TIMEOUT)
    return featuredbusiness

@register.assignment_tag
def get_home_page_business_offers(limit):
    cache_key='homeoffers'+str(limit)
    homeoffers=cache.get(cache_key)
    if homeoffers is None:
        homeoffers = BusinessCoupons.objects.filter(business__status='P',end_date__gte=date.today()).only('title','business','photo').select_related('business').order_by('-id')[:limit]
        cache.set(cache_key,homeoffers,CACHE_TIMEOUT)
    return homeoffers