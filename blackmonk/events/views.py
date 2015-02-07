import datetime,os,re,time,urllib
from datetime import date,timedelta
from time import strptime
from PIL import Image
from xml.dom import minidom

from django.shortcuts import render_to_response, get_list_or_404  
from django.http import *
from django.db.models import Q,Count,Min,Max
from django.core.paginator import Paginator
from django.utils import simplejson
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
from django.views.decorators.cache import cache_page,cache_control
from django.core.cache import cache
from django.conf import settings as my_settings
from django.views.decorators.vary import vary_on_headers
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from events.templatetags.bm_eventstags import get_featured_events
from events.models import Event,EventCategory,Tag,EventOccurence,EventRsvp
from gallery.models import PhotoAlbum
from common.models import ModuleNames,Address,VenueType
from common.utils import get_global_settings,ds_pagination,sort_queryset,ds_sortby_listingtype
from usermgmt.favoriteviews import add_remove_fav,get_fav
from django.core.cache import cache
CACHE_TIMEOUT=60*5

GET_RSVP_NOTES = {'N':'Not Going','Y':'Going','M':'Maybe','YW':'Yes Went','DR':'Maybe','DG':'Didn"t Go'}

GET_PAST_RSVP_NOTES = {'N':'Didn"t Go','Y':'Yes Went','M':'Maybe'}

NUMBER_DISPLAYED = 12
HOME_PAGE_EVENTS_COUNT = 3

def __get_featured_events():
   
    cache_key='cache_eventsfeatured_view'
    featured = cache.get(cache_key)
    if featured is None:
        key = {}
        key['status'] = 'P'
        key['listing_type'] = 'F'
        key['listing_end__gte'] = date.today()
        key['listing_start__lte'] = date.today()
        featured = Event.objects.filter(**key).only('title','slug','category','venue','start_date','end_date','start_time','end_time','album').prefetch_related('category').select_related('venue','album').order_by('-forder','end_date','-start_date')[:12]
        cache.set(cache_key,featured,CACHE_TIMEOUT)
    return featured

def __get_related_gallery():
    try:return PhotoAlbum.objects.filter(category__slug='events').only('title','category','slug','most_viewed').select_related('category').prefetch_related('album_photos').order_by('-published_on')
    except:return False

def display_events(request,day='all',template='default/events/events_home.html'):
    view_type = request.GET.get('view','list')
    
    popevents = Event.objects.filter(status='P').only('venue').order_by('-visits')[:10]
    ven_names = []
    try:
        for evnt in popevents:
            ven_names.append(evnt.venue)
    except:pass
    popvenues = Address.objects.filter(venue__in=ven_names)[:5]
    
    totalvenues=Address.objects.all().count()
    today=datetime.datetime.now()
    week_name=date.weekday(datetime.datetime.now())
    a = 6 - week_name
    sun=today+timedelta(a)
    sat=today+timedelta(a-1)
    tomorrow=today+timedelta(1)
    nxt_week=today+timedelta(7)
    nxt_month=today+timedelta(30)
    seo = ModuleNames.get_module_seo(name='events')
    categories = EventCategory.objects.only('name','slug').order_by('name')
    evdate = request.GET.get('evdate')
    if evdate:
        day = "evdate"
        evdate = datetime.datetime.strptime(evdate, '%d/%m/%Y')
    day_type = ''
    common_query = {'status':'P'}
    message = _('Sorry! There are no events found')
    try:
        free_events = request.GET['status']
        if free_events == 'free-events':
            common_query['tkt_prize'] = 'FREE'
    except:free_events = False
    event_all = ds_sortby_listingtype(Event)
    if day=='this_week':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(Q(date=sat)|Q(date=sun))
        event_all = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=sun,end_date__gte=sat),**common_query).prefetch_related('category')
        day_type=_("This Week End") 
    elif day=='today':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=today)
        event_all = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=today,end_date__gte=today),**common_query).prefetch_related('category',)
        day_type = _("Today") 
    elif day=='evdate':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=evdate)
        event_all = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=evdate,end_date__gte=evdate),**common_query).prefetch_related('category',)
        day_type = _("On ") + request.GET['evdate'] 
    elif day=='tomorrow':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=tomorrow)
        event_all = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=tomorrow,end_date__gte=tomorrow),**common_query).prefetch_related('category',)
        day_type=_("Tomorrow") 
    elif day=='nxt_week':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date__range=(today,nxt_week))
        event_all = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=nxt_week,end_date__gte=today),**common_query).prefetch_related('category',)
        day_type=_("Next 7 Days") 
    elif day=='nxt_month':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date__range=(today,nxt_month))
        event_all = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(start_date__lte=nxt_month,end_date__gte=today),**common_query).prefetch_related('category',)
        day_type=_("Next 30 Days") 
    else:
        #events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=today)
        event_all = event_all.filter(**common_query).prefetch_related('category',)
    
    #Caching
    cache_key='cache_events_'+day
    cache_event_all = cache.get(cache_key)
    if cache_event_all is None:
    #featured = Event.objects.filter(status='P',listing_type='F').order_by('-forder','end_date','-start_date')[:12]
        event_all = event_all.only('title','slug','category','venue','album','start_date','end_date','start_time','end_time').select_related('venue','album')
        #cache.set(cache_key,event_all,CACHE_TIMEOUT)
    else:
        event_all=cache_event_all
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    try:
        if day_type:
                message = _('Sorry! There are no events found in %s')%(day_type)
    except:
        pass
    data = ds_pagination(event_all,page,'event_all',NUMBER_DISPLAYED)
    #data['event_all'] = sorted(data['event_all'],key=lambda obj:sort_queryset(obj.listing_type))
    if day not in ['all', 'evdate']:
        data['url'] = reverse('events_home_event')+day+'.shtml/'
    else:
        data['url'] = reverse('events_home_event')
        if day=='evdate':
            data['evdate'] = request.GET['evdate']
    scroll = request.GET.get('scroll',False)
    
    data['totalvenues'] = totalvenues
    data['venues']=popvenues
    data['message']=message
    data['categories']=categories
    data['featured'] = __get_featured_events()
    data['seo']=seo
    data['day']=day
    data['sitesearch']='event'
    data['view_type'] = view_type
    data['today']=today.date()
    data['events_gallery'] =  __get_related_gallery()
    data['scroll'] = scroll
    if free_events == 'free-events':
            data['free_events'] = True
    return render_to_response(template,data,context_instance=RequestContext(request))

def view_venue(request,venslug=None,template='default/events/venue-details.html'):
    data={}
    data['categories']=EventCategory.objects.all().order_by('name')
    if venslug:
        venue=Address.objects.get(slug=venslug)
        event_all = ds_sortby_listingtype(Event)
        event_all = event_all.filter(venue=venue,status='P').distinct()
        if venue.telephone1 or venue.mobile or venue.email or venue.website:
            data['contact']=True
        else:
            data['contact']=False
        data['venue']= venue
        data['event_all']= event_all
        data['view_type'] = 'grid'      
    else:pass
    return render_to_response(template,data,context_instance=RequestContext(request))     

def display_cal_events(request,day,month,year):
    seo = ModuleNames.get_module_seo(name='events')
    date=datetime.datetime(int(year),int(month),int(day))
    categories=EventCategory.objects.all().order_by('name')
    events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=date)
    event_all = ds_sortby_listingtype(Event)
    featured = event_all.filter(status='P',listing_type='F')[:12]
    event_all = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=date,end_date__gte=date),status='P').prefetch_related('category').order_by('start_date').distinct()
    day_format = day+'/'+month+'/'+year
    try:page = int(request.GET['page'])
    except:page = 1
    
    if event_all.count()==0:
        message = _("Sorry! There are no Events found on %s.") %(day_format)
    else:
        message = False
    
    data = ds_pagination(event_all,page,'event_all',NUMBER_DISPLAYED)
    #data['event_all'] = sorted(data['event_all'],key=lambda obj:sort_queryset(obj.listing_type))
    data['url'] = reverse('events_display_cal_events',args=[year,month,day])+'?'
    data['categories']=categories
    data['seo']=seo
    data['s_date']=date
    data['featured']=featured
    data['message']=message
    
    today=datetime.datetime.now()
    data['today']=today.date()
    
    return render_to_response('default/events/events_all.html',data,context_instance=RequestContext(request))

def attribute_search(request,slug=False,template='default/events/events_home.html'):
    categories=EventCategory.objects.all().order_by('name')
    seo = ModuleNames.get_module_seo(name='events')
    view_type = request.GET.get('view','list')
    bc=False
    urlappend=''
    
    att_type = 'Attribute'
    try:
        category=EventCategory.objects.get(id=request.GET['cat'])
    except:category=False
    
    common_query = {'status':'P'}
    try:
        free_events = request.GET['status']
        if free_events == 'free-events':
            common_query['tkt_prize'] = 'FREE'
    except:free_events = False
     
    event_all = ds_sortby_listingtype(Event)
    try:
        if slug=='v':
            bc=request.GET['ven']
            event_all = event_all.filter(venue=bc,**common_query).prefetch_related('category',).select_related('venue') #.order_by('end_date','-start_date')
            att_type = "venue"
            urlappend = '?ven=%s'%(bc)
        if slug!='':
            category=EventCategory.objects.get(slug=slug)
            event_all = event_all.filter(category=category,**common_query).prefetch_related('category',).select_related('venue') #.order_by('end_date','-start_date')
            att_type = "category"
            seo = category
            bc = category.name
    except:return HttpResponseRedirect(reverse('events_home_event'))
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    
    message = False
    if not event_all:
        message = _("Search returned zero results")
    
    data = ds_pagination(event_all,page,'event_all',NUMBER_DISPLAYED)
    data['url'] = '/events/%s'%(slug)+'/'
    data['categories']=categories
    data['category']=category
    data['seo']=seo
    data['bc']=bc
    data['message']=message
    data['featured'] = __get_featured_events()
    data['view_type'] = view_type
    data['events_gallery'] =  __get_related_gallery()
    today=datetime.datetime.now()
    data['today']=today.date()
    if free_events == 'free-events':
            data['free_events'] = True
    return render_to_response(template,data, context_instance=RequestContext(request))     

def free_events(request,day=False,template='default/events/events_free.html'):
    event_all = ds_sortby_listingtype(Event)
    popevents = event_all.filter(status='P').only('venue').order_by('-visits')[:10]
    ven_names = []
    for evnt in popevents:
        ven_names.append(evnt.venue)
    popvenues = Address.objects.filter(venue__in=ven_names)[:4]
    today=datetime.datetime.now()
    week_name=date.weekday(datetime.datetime.now())
    a = 6 - week_name
    sun=today+timedelta(a)
    sat=today+timedelta(a-1)
    tomorrow=today+timedelta(1)
    nxt_week=today+timedelta(7)
    nxt_month=today+timedelta(30)
    seo = ModuleNames.get_module_seo(name='events')
    categories=EventCategory.objects.all().order_by('name')
    common_query = {'status':'P', 'tkt_prize':'FREE'}
    day_type=_("Free Events")
    featured = event_all.filter(status='P', listing_type='F').prefetch_related('category')[:12]
    event_all = event_all.filter(**common_query).distinct()
    if event_all.count()==0:
        message = _('Sorry! There are no events found in %s')%(day_type)
    
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    data = ds_pagination(event_all,page,'event_all',NUMBER_DISPLAYED)
    if day:
        data['url'] = '/events/'+day+'.shtml'+'?'
    else:
        data['url'] = reverse('events_free_events')+'?'
    data['message']=False
    data['categories']=categories
    data['featured']=featured
    data['popvenues']=popvenues
    data['seo']=seo
    data['day']=day
    data['sitesearch']='event'
    data['free_events'] = True
    return render_to_response(template,data,context_instance=RequestContext(request))

def event_detail(request,slug,template='default/events/event_details.html'):
    today = datetime.datetime.now() 
    categories=EventCategory.objects.all().order_by('name')
    event_all = ds_sortby_listingtype(Event)
    try:
        event = event_all.prefetch_related('category',).select_related('venue','payment').get(slug=slug)
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=today)
        #featured_events = event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=today,end_date__gte=today),status='P',category__in=event.category.all).prefetch_related('category').distinct()[:5]
        #pplrevents = event_all.filter(status='P').prefetch_related('category').exclude(slug=slug).order_by('visits')[:5]
    except:
        url=reverse('events_home_event')+'?'
        return HttpResponseRedirect(url)
    
    try:
        (message)=request.GET['message']
    except: pass
    try:
        if request.session['eventview%s'%(event.id)] != event.id:
            request.session['eventview%s'%(event.id)] = event.id
            event.visits = event.visits + 1
            event.save()
    except:
        request.session['eventview%s'%(event.id)] = event.id 
        event.visits = event.visits + 1
        event.save()
    # Generating the dates to display on the tab
    date_arr=[]
    for i in range(0,7):    
        next_date=datetime.timedelta(i)
        date_arr.append(today+next_date)
        
    #object_id = event.id
    #content_type = 'event'
    #data['suggested_item'] = event
    #data['suggested_by'] = request.user.profile.display_name.title() 
    
    return render_to_response(template,locals(),context_instance=RequestContext(request))

def go_event(request):
    try:event = Event.objects.get(id=request.GET['eid'])
    except:return HttpResponse('error')
    try:
        if request.session['eventgo%s'%(event.id)] != event.id:
            request.session['eventgo%s'%(event.id)] = event.id
            event.visitors = event.visitors + 1
            event.save()
        else:
            return HttpResponse('error')
    except:
        try:
            request.session['eventgo%s'%(event.id)] = event.id
            event.visitors = event.visitors + 1
            event.save()
        except:return HttpResponse('error')
    return HttpResponse('working')    

def ajax_tell_a_friend(request):
    scaptcha={}
    global_settings = get_global_settings()
    if request.method == 'POST':
        event = Event.objects.get(id=request.POST['content_id'])
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        to_email = request.POST['to_email']
        msg = request.POST['msg']
        subject = global_settings.domain+' - '+from_name+_('sent you event details of the "')+event.title+' "'
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['event'] = event
        email_message = render_to_string("default/events/tell_frnd_email.html",tell_a_friend_data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_email])
        email.content_subtype = "html"
        email.send()
        scaptcha['success'] = 1
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)
        
    else:
        scaptcha['success'] = 0
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)
    

def search_event(request):
    categories=EventCategory.objects.all().order_by('name')
    seo = ModuleNames.get_module_seo(name='events')
    today=datetime.datetime.now()
    try:
        if 'keyword' in request.GET:
            kw = request.GET.get('keyword').strip()
        else:
            kw = ' '
        cat = str(request.GET.get('category'))
        key = {}
        key['status']='P'
        
        if 'tag' in request.GET:
            tags = request.GET['tag']
            tag = Tag.objects.get(tag = tags)
            key['tags'] = tag.id
            
        key_or = (Q(title__icontains=kw) | Q(venue__venue__icontains=kw) | Q(event_description__icontains=kw))
        event_all = ds_sortby_listingtype(Event)
        
        if cat == 'All Categories':event_all = event_all.filter(key_or,**key).distinct()
        else:
            category = EventCategory.objects.get(name = cat)
            event_all = event_all.filter(key_or,category=category,**key).distinct()
            
        if event_all.count()==0: message = _("Sorry! '%s' did not return any results. Try another keyword.")%(kw)
        else:message = False
        try:page = int(request.GET['page'])
        except:page = 1
        data = ds_pagination(event_all,page,'event_all',NUMBER_DISPLAYED)
        data['seo']=seo
        data['search'] = True
        data['view_type'] = 'list'
        data['categories'] = categories
        data['sitesearch']='event'
        data['message']=message
        data['category'] = cat.replace(' ', '+')
        data['keyword'] = kw
        data['today']=today.date()
        return render_to_response('default/events/events_home.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('events_home_event'))

def event_retrieve_list(request,template='default/events/ajax_events.html'):
    
    retrieve_events = request.GET['retrieve_events']
    date = datetime.datetime(*strptime(request.GET['date'], "%d,%m,%Y")[0:3])
    featured_events = []
    event_all = ds_sortby_listingtype(Event)
    if retrieve_events == 'events_retrieve':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=date)
        featured_events=event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=date,end_date__gte=date),status='P').order_by('start_date').distinct()[:3]
    elif retrieve_events == 'events_article_retrieve':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=date)
        featured_events=event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=date,end_date__gte=date),status='P').order_by('-is_feature','start_date').distinct()[:3]
    elif retrieve_events == 'events_related':
        try:cat_ids=request.GET['eids'].split(',')
        except:cat_ids=request.GET['eids']
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=date)
        featured_events=event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=date,end_date__gte=date),status='P',category__in=cat_ids).order_by('start_date').distinct()[:3]
    elif retrieve_events == 'fifa':
        events_sched_list = EventOccurence.objects.values_list('event_id', flat=True).filter(date=date)
        featured_events=event_all.filter(Q(is_reoccuring=True,id__in = events_sched_list)|Q(is_reoccuring=False,start_date__lte=date,end_date__gte=date),status='P',tags__tag__icontains = 'fifa').order_by('-is_feature','start_date').distinct()[:3]
    data = {'featured_events' : featured_events }
    return render_to_response(template,data)   
    
def venue_list(request,cat=False):
    seo = ModuleNames.get_module_seo(name='events')
    venues=Address.objects.all().order_by('venue')
    categories=EventCategory.objects.all().order_by('name')
    try:page = int(request.GET['page'])
    except:page = 1
    data = ds_pagination(venues,page,'venues',6)
    data['url'] = reverse('events_venue_list')
    data['seo']=seo
    data['categories']=categories
    data['venue_types'] = VenueType.objects.all().order_by('title')
    return render_to_response('default/events/venue_list.html',data,context_instance=RequestContext(request))     

def search_venue_list(request,cat=False):
    categories=EventCategory.objects.all().order_by('name')
    seo = ModuleNames.get_module_seo(name='events')
    
    try:venuetype=VenueType.objects.get(slug=cat)
    except:venuetype=None
    
    if venuetype:venues = Address.objects.filter(type=venuetype,venue__isnull=False).order_by('venue')
    else:venues=Address.objects.filter(venue__isnull=False).order_by('venue')  
    
    try:venues=venues.exclude(venue='')
    except:venues=venues
    
    try:page = int(request.GET['page'])
    except:page = 1
    data = ds_pagination(venues,page,'venues',6)
    data['url'] = '/venues/type/%s'%(cat)+'?' 
    data['seo']=seo
    data['venue_types'] = VenueType.objects.all().order_by('title')
    data['venuetype']=venuetype
    data['categories']=categories
    return render_to_response('default/events/venue_list.html',data,context_instance=RequestContext(request))  
 
def auto_suggest(request):
    try:data = Address.objects.filter(venue__icontains=request.GET['term'])[:10]
    except:data = Address.objects.all()[:10]
    main=[]
    for ve in data:
       if  ve.zip:
           values=','.join([str(ve.venue), str(ve.address1),str(ve.zip)])
       else:
            values=','.join([str(ve.venue), str(ve.address1)]) 
       b={'label':values,'id':str(ve.id),'label':values}
       main.append(b)

    #return HttpResponse(simplejson.dumps(main))
    return HttpResponse(simplejson.dumps(main), content_type="application/json")

def auto_suggest_tag(request):
    try:
        data = Tag.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:
        data = Tag.objects.all()[:10]
    response_dict = {}
    child_dict = []
    response_dict.update({'results':child_dict})
    mytags=[]
    for tag in data :
       
        b={'label':tag.tag,'id':tag.id,'value':tag.tag}
        mytags.append(b)

    return HttpResponse(simplejson.dumps(mytags))

def event_add_to_fav(request):
    try:
        event = Event.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(event,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')
    
@login_required    
def event_event_rsvp(request, template='default/events/rsvp-status.html'): 
    ''' ajax method for event rsvp'''
    data = {}
    send_data = {}
    try:
        event = Event.objects.get(id=request.GET['eid'])
        status = request.GET.get('status','N')
        try:
            rsvp_obj = EventRsvp.objects.get(event=event,created_by=request.user)
        except:
            rsvp_obj = EventRsvp(event=event,created_by=request.user)
        rsvp_obj.status = status
        if event.check_occured():
            rsvp_obj.notes = GET_PAST_RSVP_NOTES[status]
        else:rsvp_obj.notes = GET_RSVP_NOTES[status]    
        rsvp_obj.save()
        data['event'] = event
        data['rsvp_obj'] = rsvp_obj
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        #send_data['rsvp_msg'] = rsvp_obj.notes
        send_data['going_count'] = EventRsvp.objects.filter(event=event,status='Y').count()
        send_data['maybe_count'] = EventRsvp.objects.filter(event=event,status='M').count()
        send_data['success'] = True    
    except:
        send_data['success'] = False
    return HttpResponse(simplejson.dumps(send_data))

def event_get_rsvp_status(request, template='default/events/rsvp-status.html'):
    ''' ajax method for event rsvp status of user loged in'''
    data={}
    send_data = {}
    try:
        event = Event.objects.get(id=request.GET['eid'])
        rsvp_obj = EventRsvp.objects.get(event=event,created_by=request.user)
        if event.check_occured():
            data['rsvp_msg'] = GET_PAST_RSVP_NOTES[rsvp_obj.status]
        else:data['rsvp_msg'] = GET_RSVP_NOTES[rsvp_obj.status]    
        data['event'] = event
        data['rsvp_obj'] = rsvp_obj
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['success'] = True
    except:
        send_data['success'] = False   
    try:
        send_data['going_count'] = EventRsvp.objects.filter(event=event,status='Y').count()
        send_data['maybe_count'] = EventRsvp.objects.filter(event=event,status='M').count()
    except:send_data['going_count'] = send_data['maybe_count'] = 0        
    return HttpResponse(simplejson.dumps(send_data))

def ajax_get_events_by_date(request,template='default/events/ajax_events.html'):
    ''' home page ajax method for retreiving events by date '''
    data={}
    send_data = {}
    try:
        try:
            selected_date = datetime.datetime(*strptime(request.GET['sel_date'], "%Y-%m-%d")[0:3])
        except:
            selected_date = date.today()
        data['events'] = Event.objects.filter(start_date__lte=selected_date,end_date__gte=selected_date,status='P').only("title","venue","slug","start_date","end_date","start_time","end_time").prefetch_related('category').order_by('?')[:HOME_PAGE_EVENTS_COUNT]
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['status'] = True
    except:send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def ajax_popular_venue(request):
    data={}
    popevents = Event.objects.filter(status='P').only('venue').order_by('-visits')[:10]
    ven_names = []
    try:
        for evnt in popevents:
            ven_names.append(evnt.venue)
        popvenues = Address.objects.filter(venue__in=ven_names)[:4]
    except:popvenues = False
    data['popvenues_html'] = render_to_string('default/events/popular_venue.html',{'popvenues': popvenues},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps(data))
