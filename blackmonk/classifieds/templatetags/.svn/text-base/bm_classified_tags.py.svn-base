import datetime

from django.template import Library
from django.core.cache import cache
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from mptt_comments.models import MpttComment
from classifieds.models import Classifieds
from django.core.cache import cache
CACHE_TIMEOUT=60*10
register = Library()

CLASSIFIED_MAX_PRICE = 1000

@register.assignment_tag
def get_latest_classifieds(limit=4):
    fetched_values = ['title','slug','published_on','tp_id','created_by','created_on','album']
    cache_key='ttag_classifieds'+str(limit)
    classifieds = cache.get(cache_key)
    if classifieds is None:
        classifieds = Classifieds.objects.filter(status='P').only(*fetched_values).select_related('created_by').order_by('-created_on')[:limit]
        cache.set(cache_key,classifieds,CACHE_TIMEOUT)
    return classifieds

@register.assignment_tag
def get_latest_classifieds_album(limit=5):
    cache_key='ttag_classifieds'+str(limit)
    classifieds = cache.get(cache_key)
    if classifieds is None:
        classifieds = Classifieds.objects.filter(status='P').exclude(album=None).order_by('-created_on')[:limit]
        cache.set(cache_key,classifieds,CACHE_TIMEOUT)
    return classifieds

@register.inclusion_tag('default/custom_tags.html')
def show_recent_classified_review(template='default/movies/recent-reviews.html'):
    recent_reviews =[]
    try:
        c_type = ContentType.objects.get(model='classifieds')
        recent_reviews = MpttComment.objects.filter(content_type=c_type,level__gte=1,is_public=True,is_removed=False).order_by('-submit_date')[:4]
    except:
        pass
    return {'template': template, 'recent_reviews': recent_reviews}

@register.assignment_tag
def get_classifieds_max_price(selected_category=False):
    try:
        if selected_category:
            max_price = Classifieds.objects.filter(category = selected_category).aggregate(Max('classified_price')) 
        else:
            max_price = Classifieds.objects.all().aggregate(Max('classified_price'))   
        if not max_price['classified_price__max']:
            max_price['classified_price__max'] = CLASSIFIED_MAX_PRICE
    except:
        max_price = CLASSIFIED_MAX_PRICE
    return max_price 