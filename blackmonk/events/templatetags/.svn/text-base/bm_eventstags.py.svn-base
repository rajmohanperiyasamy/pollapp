from datetime import date, timedelta
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Q
from django.template import Library
from django.utils import timezone

from events.models import Event, EventOccurence
from mptt_comments.models import MpttComment

CACHE_TIMEOUT=60*10
register = Library()

@register.assignment_tag
def get_popular_events(**kwargs):
    in_upcoming_days = kwargs.get('in_upcoming_days', 30) 
    limit = kwargs.get('limit', 5)
    cache_key='ttag_popular_events'+str(limit)+str(in_upcoming_days)
    popular_events=cache.get(cache_key)
    if popular_events is None:
        interval_start_date = date.today()
        interval_end_date = interval_start_date + timedelta(in_upcoming_days)
        popular_events = Event.objects.only("title","venue","slug","start_date","end_date","start_time","end_time").filter(start_date__lte = interval_end_date, end_date__gte = interval_start_date, status='P').select_related("venue").prefetch_related('category').order_by('-visits')[:limit]
        cache.set(cache_key,popular_events,CACHE_TIMEOUT)
    return popular_events

@register.inclusion_tag('default/custom_tags.html')
def show_today_tickets(template='default/events/tickets_aside.html'):
    today = timezone.now()
    events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=today)
    todayevents = Event.objects.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=today,end_date__gte=today)).exclude(ticket_site=None).order_by('?')[:4]
    return {'template': template, 'todayevents': todayevents}

@register.inclusion_tag('default/custom_tags.html')
def show_recent_events_review(template='default/movies/recent-reviews.html'):
    recent_reviews =[]
    try:
        c_type = ContentType.objects.get(model='event')
        recent_reviews = MpttComment.objects.filter(content_type=c_type,level__gte=1,is_public=True,is_removed=False).order_by('-submit_date')[:4]
    except:
        pass
    return {'template': template, 'recent_reviews': recent_reviews}

@register.assignment_tag
def get_featured_events(**kwargs):
    in_upcoming_days = kwargs.get('in_upcoming_days', 30) 
    limit = kwargs.get('limit', 5)
    cache_key='ttag_featured_events'+str(limit)+str(in_upcoming_days)
    featured_events=cache.get(cache_key)
    if featured_events is None:
        interval_start_date = date.today()
        interval_end_date = interval_start_date + timedelta(in_upcoming_days)
        featured_events = Event.objects.only("title","venue","slug","start_date","end_date","start_time","end_time").filter(start_date__lte = interval_end_date, end_date__gte = interval_start_date, listing_start__lte = interval_start_date, status='P', listing_type='F').select_related("venue").prefetch_related('category').order_by('start_date')[:limit]
        cache.set(cache_key,featured_events,CACHE_TIMEOUT)
    return featured_events    

@register.assignment_tag
def get_upcoming_events(**kwargs):
    today = date.today()
    cache_key='ttag_upcoming_events'
    upcoming_events=cache.get(cache_key)
    if upcoming_events is None:
        upcoming_events = Event.objects.only("title","venue","slug","start_date","end_date","start_time","end_time").filter(start_date__gt = today, status='P', listing_type='F').order_by('start_date')
        cache.set(cache_key,upcoming_events,CACHE_TIMEOUT)
    return upcoming_events