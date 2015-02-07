
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q, Count
from django.utils import simplejson
from django.contrib.gis.geoip import GeoIP
from django.conf import settings as my_settings
from googlemaps import GoogleMaps

from common.models import Address
from business.models import Business
from attraction.models import Attraction
from events.models import Event
from classifieds.models import Classifieds
from movies.models import Theatres

from common.utils import ds_pagination, ds_sortby_listingtype
from locality.maputils import __get_map_info_window_contents, __get_location_from_ip

NUMBER_DISPLAYED = 12
orderval = ['id','name','most_viewed','ratings','-id','-name','-most_viewed','-ratings']
SORT_VALUES = {'bm':'-id', 'ratings':'-ratings'}
SEO_LIST = {'title':'Near by %s', 'description':'Find local %s, view maps and get driving directions in Maps'}

geoip_obj = GeoIP()

class MapSeo():
    def __init__(self, seo_title, seo_description):
        self.seo_title = seo_title
        self.seo_description = seo_description
    
def __filter_business(request):
    page = int(request.GET.get('page',1))
    search = request.GET.get('search',False)
    location = __get_location_from_ip(request)
    key={}
    q = request.GET.get('q','')
    q_text=()
    key['status'] = 'P'
    if search:
        try:
            q_text=(Q(name__icontains=q)|Q(categories__name__icontains=q)|Q(categories__parent_cat__name__icontains=q)|Q(tags__tag__icontains=q))
        except:pass
    try:
        key['address__id__in'] = Address.objects.filter(Q(address1__icontains=location)|Q(address2__icontains=location)|Q(city__icontains=location),business__status='P').values_list("id", flat=True)
    except:pass
    
    if q_text:
        businessall = temp_vars = Business.objects.filter(q_text,**key).prefetch_related('logo','categories','album').order_by('-id')
    else:businessall = temp_vars = Business.objects.filter(**key).prefetch_related('logo','categories','album').order_by('-id')
    
    businessall = businessall.distinct()[:30]
    data = ds_pagination(businessall,page,'businesslist',NUMBER_DISPLAYED)
    
    if data['businesslist']:
        data['other_business'] = temp_vars.exclude(id__in=data['businesslist'])[:30]
    else:
        data['other_business'] = False
    data['q'] = q
    data['fl_counter'] = int(request.GET.get('fl_counter',0))
    data['search'] = search
    return data

def map_home(request, template='default/locality/map/map-home.html'):
    data = __filter_business(request)
    try:
        data['seo'] = MapSeo(SEO_LIST['title']%('business'), SEO_LIST['description']%('business'))
    except:
        data['seo'] = None
    return render_to_response(template, data, context_instance=RequestContext(request))

def map_ajax_filter_business(request,template='default/locality/map/ajax-business-list.html'):
    send_data={}
    try:
        data = __filter_business(request)
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['page_number'] = data['next']
        send_data['fl_counter'] = data['fl_counter']
        send_data['status'] = True
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def __filter_events(request):
    page = int(request.GET.get('page',1))
    search = request.GET.get('search',False)
    location = __get_location_from_ip(request)
    key={}
    q = request.GET.get('q','')
    q_text=()
    key['status'] = 'P'
    if search:
        try:
            q_text = (Q(title__icontains=q) | Q(venue__venue__icontains=q) | Q(event_description__icontains=q) | Q(category__name__icontains=q))
        except:pass
    try:
        key['venue__id__in'] = Address.objects.filter(Q(address1__icontains=location)|Q(address2__icontains=location)|Q(city__icontains=location),event__status='P').values_list("id", flat=True)
    except:
        pass
    
    if q_text:
        eventsall = temp_vars = Event.objects.filter(q_text,**key).prefetch_related('category').order_by('-id')
    else:eventsall = temp_vars = Event.objects.filter(**key).prefetch_related('category').order_by('-id')
    
    eventsall = eventsall.distinct()[:30]
    data = ds_pagination(eventsall,page,'events',NUMBER_DISPLAYED)
    
    if data['events']:
        data['other_events'] = temp_vars.exclude(id__in=data['events'])[:30]
    else:
        data['other_events'] = False
    data['q'] = q
    data['fl_counter'] = int(request.GET.get('fl_counter',0))
    data['search'] = search
    return data
    
def map_events(request, template='default/locality/map/map-events.html'):
    data = __filter_events(request)
    try:
        data['seo'] = MapSeo(SEO_LIST['title']%('events'), SEO_LIST['description']%('events'))
    except:
        data['seo'] = None
    return render_to_response(template, data, context_instance=RequestContext(request))

def map_ajax_filter_events(request,template='default/locality/map/ajax-events-list.html'):
    send_data={}
    try:
        data = __filter_events(request)
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['page_number'] = data['next']
        send_data['fl_counter'] = data['fl_counter']
        send_data['status'] = True
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def __filter_classifieds(request):
    page = int(request.GET.get('page',1))
    search = request.GET.get('search',False)
    location = __get_location_from_ip(request)
    key={}
    q = request.GET.get('q','')
    q_text=()
    key['status'] = 'P'
    if search:
        try:
            q_text =(Q(title__icontains=q)|Q(category__name__icontains=q)|Q(description__icontains=q))
        except:pass
    try:
        key['address__id__in'] = Address.objects.filter(Q(address1__icontains=location)|Q(address2__icontains=location)|Q(city__icontains=location),classifieds__status='P').values_list("id", flat=True)
    except:
        pass
    
    if q_text:
        classifiedsall = temp_vars = Classifieds.objects.filter(q_text,**key).prefetch_related('category').order_by('-id')
    else:classifiedsall = temp_vars = Classifieds.objects.filter(**key).prefetch_related('category').order_by('-id')
    
    classifiedsall = classifiedsall.distinct()[:30]
    data = ds_pagination(classifiedsall,page,'classifieds',NUMBER_DISPLAYED)
    
    if data['classifieds']:
        data['other_classifieds'] = temp_vars.exclude(id__in=data['classifieds'])[:30]
    else:
        data['other_classifieds'] = False
    data['q'] = q
    data['fl_counter'] = int(request.GET.get('fl_counter',0))
    data['search'] = search
    return data

def map_classifieds(request, template='default/locality/map/map-classifieds.html'):
    data = __filter_classifieds(request)
    try:
        data['seo'] = MapSeo(SEO_LIST['title']%('classifieds'), SEO_LIST['description']%('classifieds'))
    except:
        data['seo'] = None
    return render_to_response(template, data, context_instance=RequestContext(request))

def map_ajax_filter_classifieds(request,template='default/locality/map/ajax-classifieds-list.html'):
    send_data={}
    try:
        data = __filter_classifieds(request)
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['page_number'] = data['next']
        send_data['fl_counter'] = data['fl_counter']
        send_data['status'] = True
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def __filter_cinemas(request):
    page = int(request.GET.get('page',1))
    search = request.GET.get('search',False)
    location = __get_location_from_ip(request)
    key={}
    q = request.GET.get('q','')
    q_text=()
    #key['status'] = 'P'
    if search:
        try:
            q_text =(Q(name__icontains=q)|Q(theatreseo_title__icontains=q))
        except:pass
    try:
        key['address__id__in'] = Address.objects.filter(Q(address1__icontains=location)|Q(address2__icontains=location)|Q(city__icontains=location),attraction__status='P').values_list("id", flat=True)
    except:
        pass
    
    if q_text:
        theatersall = temp_vars = Theatres.objects.filter(q_text,**key).select_related('address').order_by('-id')
    else:theatersall = temp_vars = Theatres.objects.filter(**key).select_related('address').order_by('-id')
    
    theatersall = theatersall.distinct()[:30]
    data = ds_pagination(theatersall,page,'theaters',NUMBER_DISPLAYED)
    
    if data['theaters']:
        data['other_theaters'] = temp_vars.exclude(id__in=data['theaters'])[:30]
    else:
        data['other_theaters'] = False
    data['q'] = q
    data['fl_counter'] = int(request.GET.get('fl_counter',0))
    data['search'] = search
    return data
    
def map_cinemas(request, template='default/locality/map/map-cinemas.html'):
    data = __filter_cinemas(request)
    try:
        data['seo'] = MapSeo(SEO_LIST['title']%('cinemas'), SEO_LIST['description']%('cinemas'))
    except:
        data['seo'] = None
    return render_to_response(template, data, context_instance=RequestContext(request))

def map_ajax_filter_cinemas(request, template='default/locality/map/ajax-theatres-list.html'):
    send_data={}
    try:
        data = __filter_cinemas(request)
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['page_number'] = data['next']
        send_data['fl_counter'] = data['fl_counter']
        send_data['status'] = True
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def __filter_attractions(request):
    page = int(request.GET.get('page',1))
    search = request.GET.get('search',False)
    location = __get_location_from_ip(request)
    key={}
    q = request.GET.get('q','')
    q_text=()
    key['status'] = 'P'
    if search:
        try:
            q_text =(Q(name__icontains=q)|Q(category__name__icontains=q)|Q(description__icontains=q))
        except:pass
    try:
        key['venue__id__in'] = Address.objects.filter(Q(address1__icontains=location)|Q(address2__icontains=location)|Q(city__icontains=location),attraction__status='P').values_list("id", flat=True)
    except:
        pass
    
    if q_text:
        attractionall = temp_vars = Attraction.objects.filter(q_text,**key).select_related('venue','album').prefetch_related('category').order_by('-id')
    else:attractionall = temp_vars = Attraction.objects.filter(**key).select_related('venue','album').prefetch_related('category').order_by('-id')
    
    attractionall = attractionall.distinct()[:30]
    data = ds_pagination(attractionall,page,'attractions',NUMBER_DISPLAYED)
    
    if data['attractions']:
        data['other_attractions'] = temp_vars.exclude(id__in=data['attractions'])[:30]
    else:
        data['other_attractions'] = False
    data['q'] = q
    data['fl_counter'] = int(request.GET.get('fl_counter',0))
    data['search'] = search
    return data

def map_attractions(request, template='default/locality/map/map-attractions.html'):
    data = __filter_attractions(request)
    try:
        data['seo'] = MapSeo(SEO_LIST['title']%('attractions'), SEO_LIST['description']%('attractions'))
    except:
        data['seo'] = None
    return render_to_response(template, data, context_instance=RequestContext(request))

def map_ajax_filter_attractions(request,template='default/locality/map/ajax-attractions-list.html'):
    send_data={}
    try:
        data = __filter_attractions(request)
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['page_number'] = data['next']
        send_data['fl_counter'] = data['fl_counter']
        send_data['status'] = True
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def map_get_direction(request, template='default/locality/map/get-directions.html'):
    data = {}
    try:
        address_obj = Address.objects.get(id = request.GET['aid'])
    except:
        address_obj = None    
    data['address_obj'] = address_obj
    data['navigation'] = request.GET.get('src','business')
    data['content_obj'] = __get_map_info_window_contents(data['navigation'],request.GET['objid'])
    return render_to_response(template, data, context_instance=RequestContext(request))

def ajax_map_get_direction(request, template='default/locality/map/ajax-get-directions.html'):
    data = {}
    send_data = {}
    try:
        address_obj = Address.objects.get(id = request.GET.get('aid',None))
        data['address_obj'] = address_obj
        data['navigation'] = request.GET.get('src','business')
        data['content_obj'] = __get_map_info_window_contents(data['navigation'],request.GET['objid'])
        send_data['html'] = render_to_string(template,data,context_instance=RequestContext(request))
        send_data['status'] = True
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))
