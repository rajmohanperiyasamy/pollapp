import csv
from datetime import *
import datetime
from django.conf import settings as my_settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.encoding import smart_unicode
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from time import strptime

from common import signals
from common.fileupload import upload_photos_forgallery, delete_photos
from common.getunique import getUniqueValue
from common.mail_utils import mail_publish_event
from common.models import Address, VenueType, CSVfile
from common.staff_messages import EVENT_MSG, COMMON
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name, get_status_class
from common.utils import ds_pagination, get_lat_lng, get_global_settings, \
    ds_cleantext, get_map_lat_lng_zoom
from common.utilviews import crop_and_save_coverphoto
from events.forms import EventFormStaff, EditEventFormStaff, EventSeoForm
from events.models import Event, EventCategory, EventPrice, EventRule, \
    EventOccurence, Tag as EventTag
from events.tasks import process_events_csv_upload
from events.utils import event_repeat_save, co_add_categories, co_add_tags
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from locality.forms import VenueForm
from payments.models import PaymentOrder, OfflinePayment
from payments.utils import get_invoice_num
from django.contrib.contenttypes.models import ContentType


#from photo_library  import signals
event_album_cat = PhotoCategory.objects.get_or_create(name="Events", slug='events', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
NO_OF_ITEMS_PER_PAGE=10


@staff_member_required
def display_events(request,template='events/staff/home.html'):  
    eventcategory = EventCategory.objects.all().order_by('name')
    eventsdisplay = Event.objects.all().exclude(status='D').order_by('-created_on')
    event_state = Event.objects.values('status').exclude(status='D').annotate(s_count=Count('status'))
    
    msg = request.GET.get('msg',"")
    
    total = 0
    STATE={'P':0,'N':0,'R':0,'B':0,'E':0}
    for st in event_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    
    data = ds_pagination(eventsdisplay,'1','eventsdisplay',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =EVENT_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['categorys'] = eventcategory
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['expired'] =STATE['E']
    data['search'] =False
    try:data['recent'] = request.GET['pending_events']
    except:data['recent'] = False
    return render_to_response(template,data, context_instance=RequestContext(request))
 
@staff_member_required
def ajax_event_action(request,template='events/staff/ajax_delete_listing.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    eventlist = Event.objects.filter(id__in=id)
    status=0
    if action=='DEL':
        if request.user.has_perm('events.delete_event'):
            signals.celery_delete_indexs.send(sender=None,objects=eventlist)
            for event in eventlist:
                try:event.album.delete()
                except:pass
            eventlist.delete()
            status=1
            msg=str(EVENT_MSG['EDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('events.publish_events'):
            eventlist.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=eventlist)
            status=1
            msg=str(EVENT_MSG[action])
            mtype=get_msg_class_name('s')
            if action=='P':
                try:
                    for e in eventlist:mail_publish_event(e)
                except:pass
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    
    for event in eventlist:
        event.save()
        for log in event.audit_log.all()[:1]:
            log.action_type = action
            log.save()
            
    data=filter_events(request)
    
    new_id=[]
    for cs in data['eventsdisplay']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
                
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagination']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype    
    send_data['status']=status
    return HttpResponse(simplejson.dumps(send_data)) 

@staff_member_required
def ajax_display_events(request,template='events/staff/ajax-event-listing.html'):
    data=filter_events(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    if data['search_status']:
        send_data['search_status'] = data['search_status']
    return HttpResponse(simplejson.dumps(send_data))

def filter_events(request):
    data=key={}
    q=()
    created_user = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-created_on')
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    search_status = request.GET.get('srch_status',None)
    if status!='all':key['status'] = status
    if listing_type!='all':key['listing_type'] = listing_type
        
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:created_user = True
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        search_status = request.GET.get('srch_status',None)
        try:start_date = datetime.datetime.strptime(request.GET['start_date'], "%d/%m/%Y")
        except:start_date = False
        try:end_date = datetime.datetime.strptime(request.GET['end_date'], "%d/%m/%Y")
        except:end_date = False
        
        if search_category:
            key['category__id'] = search_category
        if search_status:
            key['status'] = search_status
        if start_date:
            key['start_date__gte'] = start_date
        if end_date:
            key['end_date__lte'] = end_date
        
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='venue':key['venue__venue__icontains'] = search_keyword
            elif search_type=='zip':key['venue__zip__icontains'] = search_keyword
            else:key['created_by__display_name__icontains'] = search_keyword
        
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(event_description__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(venue__venue__icontains=search_keyword)|Q(venue__zip__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if not created_user:eventsdisplay = Event.objects.filter(q,**key).exclude(status='D').select_related('category','created_by').order_by(sort).distinct()
            else:eventsdisplay = Event.objects.filter(q,**key).exclude(Q(created_by = request.user)|Q(status='D')).select_related('category','created_by').order_by(sort).distinct()
        else:
            if not created_user:eventsdisplay = Event.objects.filter(**key).exclude(status='D').select_related('category','created_by').order_by(sort).distinct()
            else:eventsdisplay = Event.objects.filter(**key).exclude(Q(created_by = request.user)|Q(status='D')).select_related('category','created_by').order_by(sort).distinct()
    else:
        if not created_user:eventsdisplay = Event.objects.filter(**key).exclude(status='D').select_related('category','created_by').order_by(sort)
        else: eventsdisplay = Event.objects.filter(**key).exclude(Q(created_by = request.user)|Q(status='D')).select_related('category','created_by').order_by(sort)
        
    data = ds_pagination(eventsdisplay,page,'eventsdisplay',item_perpage)
    if search_status:
        data['search_status'] = search_status
    else:
        data['search_status'] = None
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

@staff_member_required
def ajax_event_state(request):
    estatus = request.GET.get('status','all')
    total = 0
    STATE={'P':0,'N':0,'R':0,'B':0,'E':0}
   
    if estatus == 'all':
        event_state = Event.objects.values('status').exclude(status='D').annotate(s_count=Count('status'))
    else:
        event_state = Event.objects.filter(created_by=request.user).values('status').exclude(status='D').annotate(s_count=Count('status'))

    for st in event_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'expired':STATE['E'],
    }
    return HttpResponse(simplejson.dumps(data))

######################### ADD / EDIT EVENTS ########################

@staff_member_required
def add_event(request,template='events/staff/addEvent.html'):
    data={}
    try:
        eventobj = Event.objects.get( pk = request.REQUEST['eid'] )
        form = EditEventFormStaff(instance = eventobj)
        data['event'] = eventobj
        if not request.user.has_perm('events.change_event'):raise PermissionDenied
    except:
        eventobj = False
        form = EventFormStaff()
        if not request.user.has_perm('events.add_event'):raise PermissionDenied
    data['event_price_objects'] = EventPrice.objects.all().order_by('-id')   
    data['eventobj']=eventobj
    if eventobj:
            data['event_tags']=eventobj.tags.all()
            data['venue'] = eventobj.venue
    
    if request.method =='POST':
        if eventobj:form = EditEventFormStaff(request.POST,instance = eventobj)
        else:form = EventFormStaff(request.POST)
        
        data['new_pic']=request.POST.getlist('new_pic')
        try:data['event_tags'] = request.POST['tags'].split(',')
        except:data['event_tags'] = [request.POST['tags']]
        try:data['venue'] = Address.objects.get(id=request.POST['venue'])
        except:data['venue'] = False
        
        try:
            free_event=request.POST['free_event']
            if free_event:
                data['free_event_checked'] = 'checked'
        except:free_event = False
        if form.is_valid():
            event=form.save(commit=False)
            event.slug=getUniqueValue(Event,slugify(event.title),instance_pk=event.id)
            
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                if eventobj and eventobj.album:
                    album = eventobj.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = event_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = event.title
                album.slug = getUniqueValue(PhotoAlbum, slugify(event.slug))
                album.seo_title = event.title[:70],
                album.seo_description = album.summary = event.event_description[:160]
                album.save()
                
                event.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
                
                 
            try:
                if not event.created_by:event.created_by = request.user
            except:event.created_by = request.user
            event.modified_by=request.user
            
            try:event.venue = Address.objects.get(id=request.POST['venue'])
            except:pass
            if free_event:
                event.tkt_prize = 'FREE'
            
            submit_type = request.POST.get('save_button', 'publish')
            if submit_type == 'publish':event.status = 'P'
            else:
                if event.status == 'D' or event.status == 'E':
                    event.status = 'N'
            
            event.seo_title = ds_cleantext(event.title)
            event.seo_description = ds_cleantext(strip_tags(event.event_description[:250]))
            ## Event Repeat  
            try:
                request.POST['event_timing_repeat']
                rpt_chk = request.POST['repeat_store']
                if not rpt_chk:
                    raise Exception()
                evnt_rule = EventRule()
                event.is_reoccuring = True
                is_repeat = True
            except:
                event.is_reoccuring = False
                event.repeat_summary = ""
                if event.rule and event.rule.id:
                    event.rule.delete() 
                    event.rule=None
                is_repeat = False
                
            try:event_occurence = EventOccurence.objects.filter(event = event).delete()
            except:pass
            
            if is_repeat:     
                rule,rslt,event = event_repeat_save(request,event,evnt_rule)
                rule.save()
                event.rule = evnt_rule
                for s in rslt:
                    event_occurence = EventOccurence()
                    event_occurence.date = s
                    event_occurence.event = event
                    event_occurence.save()
            
            event.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=event)
            co_add_categories(event, request.POST.getlist('category'))
            co_add_tags(event,request.POST['tags'])
            if not eventobj:_add_event_payment(request,event)
            if 'eid' in request.REQUEST:
                messages.success(request, str(EVENT_MSG['EUP']))
            else:
                messages.success(request, str(EVENT_MSG['YES']))
            
            signals.celery_update_index.send(sender=None,object=event)
            #Deleting unnecessary audit logs which is created during creation of article.
            if 'eid' not in request.REQUEST:
                for log in event.audit_log.all():
                    if log.action_type=='U':
                        log.delete()
                        
            return HttpResponseRedirect(reverse('staff_event_home'))
        else:
            data['form'] = form
    else:
        data['form'] = form
        
    for obj in EventPrice.objects.all():
        data[obj.level_label+'_listing_price'] = obj.price
    return render_to_response(template,data,context_instance=RequestContext(request))

def _add_event_payment(request,event):
    data={}
    try:level_selected = EventPrice.objects.get(level=request.POST['listingtype'])
    except:level_selected = False
    if level_selected.level!='level0':event.is_paid=True
    else:event.is_paid=False
    if level_selected:event.payment = level_selected

    
    if not event.listing_start:event.listing_start = event.start_date
    if not event.listing_end:event.listing_end =   event.end_date
    event.save()
    
    if level_selected.level=='level1' or level_selected.level=='level2':
        if level_selected.level=='level1': 
            event.listing_type="S"
            save_to_paymentorder(request,event,'sponsored event',  event.listing_price,event.listing_start,event.listing_end)
        elif level_selected.level=='level2':
            save_to_paymentorder(request,event,'featured event',  event.listing_price,event.listing_start,event.listing_end)
            event.listing_type="F"
    else:event.listing_type="B"

    event.save()

@staff_member_required
def time_repeat(request,template='events/staff/time_repeat.html'):
    data = {}
    try:
        ye = request.GET['edit']
        if ye == 'yes':
            data['edit']=True
        else:data['edit']=False    
    except:data['edit']=False    
    return render_to_response(template,data,context_instance=RequestContext(request))


def ajax_upload_photos(request):
    if request.method == "POST":
        gal_id = request.POST.get('gal_id')
        eid = request.GET.get('id')
        if gal_id and gal_id.isdigit():
            album = PhotoAlbum.objects.get(id=gal_id)
        elif eid and eid.isdigit():
            event = Event.objects.get(id=eid)
            album = event.album
        else: 
            album = None
        response = upload_photos_forgallery(request,Photos,album,'album')
        return response
    else:
        event = Event.objects.get(id=request.GET['id'])
        album = event.album
        return upload_photos_forgallery(request,Photos,album,'album')
    
@staff_member_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,EventPhoto,pk)

@staff_member_required
def ajax_get_default_photos(request):  
    ""

def ajax_add_venue(request,template='events/staff/ajax-add-venue.html'):
    global_settings=get_global_settings()
    data={}
    try:
        venue = Address.objects.get(id=request.REQUEST['vid'])
        form=VenueForm(instance=venue)
    except:
        venue = False
        form = VenueForm()
    data['venue']=venue
    if request.method=='POST':
        if venue:
            form=VenueForm(request.POST,instance=venue)
            msg = str(EVENT_MSG['SUV'])
        else:
            form=VenueForm(request.POST)
            msg = str(EVENT_MSG['SAV'])
        if form.is_valid():
            venue=form.save(commit=False)
            
            try:
                venue.lat, venue.lon, venue.zoom = get_lat_lng(request.POST['lat_lng'])
                try:venue.zoom = int(request.POST['map_zoom'])
                except:pass
            except:venue.lat, venue.lon, venue.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            venue.created_by=venue.modified_by=request.user
            if not venue.seo_title:
                venue.seo_title = ds_cleantext(venue.venue)
            if not venue.seo_description:
                venue.seo_description = ds_cleantext(venue.description[:400])
            venue.save()
            address=str(venue.venue)+','+str(venue.address1)+','+str(venue.zip)
            template_name='events/staff/display_address.html'
            return_data = {}
            return_data['venue'] = venue
            html=render_to_string(template_name,return_data, context_instance=RequestContext(request))
            send_data={'status':1,'msg':msg,'mtype':get_msg_class_name('s'),'address':address,'id':venue.id ,'html':html}
            return HttpResponse(simplejson.dumps(send_data))
        else:
            data['form']=form  
            return error_response(request,data,template,EVENT_MSG)  
    
    else:
        data['form']=form
    return render_to_response(template ,data,context_instance=RequestContext(request))


@staff_member_required
@permission_required('events.promote_events',raise_exception=True)
def event_listing_type(request,template='events/staff/ajax_listing_type.html'):
    data={}
    data['event'] = event= Event.objects.select_related('category','created_by').get(id=int(request.REQUEST['id']))
    if request.method=='POST':
        level_selected = EventPrice.objects.get(id=request.POST['listingtype'])
        event.payment=level_selected
        try:event.listing_price=request.POST['price_'+str(level_selected.id)]
        except:pass
        if level_selected.level!='level0':event.is_paid=True
        else:event.is_paid=False
        try:
            #event.listing_start = datetime(*strptime(request.POST['start_date'],"%d/%m/%Y")[0:5])
            #event.listing_end =   datetime(*strptime(request.POST['end_date'],"%d/%m/%Y")[0:5])  
            event.listing_start = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y")
            event.listing_end = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y")
        except:
            event.listing_start = event.start_date
            event.listing_end =   event.end_date
        event.save()
        
        if level_selected.level=='level1' or level_selected.level=='level2':
            if level_selected.level=='level1': 
                event.listing_type="S"
                save_to_paymentorder(request,event,'sponsored event',  event.listing_price,event.listing_start,event.listing_end)
            elif level_selected.level=='level2':
                save_to_paymentorder(request,event,'featured event',  event.listing_price,event.listing_start,event.listing_end)
                event.listing_type="F"
        else:event.listing_type="B"
        #event.status ='P' 
        for log in event.audit_log.all()[:1]:
            log.delete()
        event.save()
        for log in event.audit_log.all()[:1]:
            if event.listing_type == 'B':log.action_type = 'N'
            else:log.action_type = event.listing_type
            log.save()
        return HttpResponse(simplejson.dumps({'status':1,'listingtype':event.listing_type,'id':event.id,'mtype':get_msg_class_name('s'),'msg':str(EVENT_MSG['ELUS'])}))
    data['event_price_objects'] = EventPrice.objects.filter(level_visibility=True).order_by('id')
    return render_to_response(template,data,context_instance = RequestContext(request))

def save_to_paymentorder(request,event,event_type,featured_price,start_date,end_date):
    from random import randint
    po=PaymentOrder(content_object = event)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Success'
    po.amount = featured_price
    po.user = request.user
    po.listing_type = event_type
    po.start_date=start_date
    po.end_date=end_date
    po.object_name=event.get_payment_title()
    po.save()
    return True

@staff_member_required
@permission_required('events.change_event',raise_exception=True)
def seo(request,id,template='events/staff/update_seo.html'):
    event = Event.objects.get(id = id)
    form=EventSeoForm(instance=event)
    if request.POST:
        form=EventSeoForm(request.POST,instance=event)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug=slugify(seo.slug)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(EVENT_MSG['ESUS'])}))
        else:
            data={'form':form,'event':event}
            return error_response(request,data,template,EVENT_MSG)
    data={'form':form,'event':event}
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('events.publish_events',raise_exception=True)
def change_status(request):
    try:
        event=Event.objects.get(id=int(request.GET['id']))
        old_status = event.status
        status = request.GET['status']
        event.status = status
        event.modified_by = request.user
        event.save()
        
        for log in event.audit_log.all()[:1]:
            log.action_type = status
            log.save()
        
        signals.celery_update_index.send(sender=None,object=event)
        #if old_status == 'N' and status == 'P':
        #    publish_event_mail(event)
        if status=='P':
            try:mail_publish_event(event)
            except:pass   
        html ='<span title="'+get_status_class(event.status)+'" name="'+event.status+'" id="id_estatus_'+str(event.id)+'" class="inline-block status-idty icon-'+get_status_class(event.status)+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')

@staff_member_required
def event_preview(request,id,template='events/staff/preview.html'):
    data = {}
    try:
        event=Event.objects.get(id=id)
        data['event'] = event
    except:pass
    return render_to_response(template,data, context_instance=RequestContext(request))

def display_address(request):
    data = {}
    try:
        venue = Address.objects.get(id=request.GET['venue_id'])
        data['venue'] = venue
        template='events/staff/display_address.html'
        html=render_to_string(template,data, context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({'status':1,'html':html}))
    except:
        venue = False
        data = {'status':0,'msg':str(EVENT_MSG['OOPS']),'mtype':get_msg_class_name('e')}
        return HttpResponse(simplejson.dumps(data))
    
# Variables used for CSV
EVNT_CSV_HEADER = ("TITLE","EVENT_DESCRIPTION","CATEGORY","STATUS","START_DATE","END_DATE","START_TIME","END_TIME","TICKET_PRIZE","TICKET_WEBSITE","TICKET_PHONE_NO","EVENT_WEBSITE","FACEBOOK","GOOGLEPLUS","CONTACT_EMAIL","PHONE","LISTING_TYPE","LISTING_PRICE","LISTING_START","LISTING_END","IS_PAID","SEO_TITLE","SEO_DESCRIPTION","TAGS","VENUE_NAME","VENUE_ADDRESS1","VENUE_ADDRESS2","VENUE_TYPE","VENUE_PHONE_NO","VENUE_MOBILE_NO","VENUE_EMAIL","VENUE_WEBSITE_URL","VENUE_DESCRIPTION","VENUE_ZIPCODE","VENUE_LATITUDE","VENUE_LONGITUDE","VENUE_MAPZOOM","VENUE_SEO_TITLE","VENUE_SEO_DESCRIPTION")
LISTING_TYPE_VAL = {'F':'FEATURED','S':'SPONSORED','B':'FREE'}
EVNT_STATUS_VAL = {'P':'PUBLISHED','N':'PENDING','R':'REJECTED','B':'BLOCKED','D':'DRAFTED','E':'EXPIRED'}
MAX_UPLOAD_FILESIZE = 2097152

@staff_member_required 
@permission_required('events.add_event',raise_exception=True) 
def events_import_csv(request):
    if request.method=='POST':
        inputfile = request.FILES['eventcsv']
        if inputfile.size > MAX_UPLOAD_FILESIZE:
            messages.error(request, "The file is too big, please make sure the size of your file is less than or equals 2Mb!")
            return HttpResponseRedirect(reverse('staff_events_import_csv'))
        else:
            csvfile = CSVfile(
                file=inputfile,
                module='events',
                status='N',
                uploaded_by=request.user
            )
            csvfile.save()
            process_events_csv_upload.delay(csvfile)
            older_files = CSVfile.objects.filter(module='events').order_by('-uploaded_on').values_list('id', flat=True)[5:]
            CSVfile.objects.filter(id__in=older_files).delete()
            messages.success(request, "Your events listings are being added,\nyou will receive notification through email once completed!")
            return HttpResponseRedirect(reverse('staff_event_home'))
    else:
        data = {
            'filehistory': CSVfile.objects.filter(module='events').order_by('-uploaded_on'),
        }
        return render_to_response('events/staff/import_csv.html', data, context_instance=RequestContext(request))


@staff_member_required  
def events_export_csv(request,template='events/staff/export_csv.html'):
    data = {}
    if request.method == "POST":
        globalsettings=get_global_settings()
        try:
            data['start_date'] = start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y")
        except:
            data['start_date'] = start_date = False
        try:
            data['end_date'] = end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y")
        except:
            data['end_date'] = end_date = False
        data['order'] = order= request.POST.get('order','-id')
        data['ltype'] = ltype=request.POST.getlist('ltype',None)
        data['status'] = status=request.POST.getlist('status',None)
        data['category']=category=request.POST.getlist('category',None)
        
        key={}
        if start_date and end_date:
            key['created_on__range']=[start_date,end_date]
        if ltype:key['listing_type__in'] = ltype    
        if status:key['status__in'] = status
        if category:key['category__id__in'] = category
        
        if key:events = Event.objects.filter(**key).exclude(status='D').order_by(order)
        else:events = Event.objects.all().exclude(status='D').order_by(order)
        
        if events.count()==0:
            data['categorys'] = EventCategory.objects.all().order_by('name')
            data['error_msg'] = _('No records were found for your search. Please try again!')
            return render_to_response (template, data, context_instance=RequestContext(request))
            
        response = HttpResponse(mimetype='text/csv')
        if start_date and end_date:
            sdate=request.POST['start_date'].replace('/','-')
            edate=request.POST['end_date'].replace('/','-')
            file_name='events_'+sdate+'_to_'+edate
        else:file_name='events'
        response['Content-Disposition'] = 'attachment;filename="%s.csv"'%(file_name)
        writer = csv.writer(response)
        writer.writerow(EVNT_CSV_HEADER) 
        for event in events:
            tags=','.join(event.tags.values_list('tag', flat=True))
            category=','.join(event.category.values_list('name', flat=True))
            try:listing_type = LISTING_TYPE_VAL[event.listing_type]
            except:listing_type = LISTING_TYPE_VAL['B']
            status = EVNT_STATUS_VAL[event.status]
            if event.venue:
                venue=event.venue
                if not venue.seo_title or not venue.seo_description:
                    venue.seo_title = ""
                    venue.seo_description = ""
            else:venue=False
            
            if event.rule:rules=event.rule
            else:rules=False
            
            if event.start_time or event.end_time:
                event.start_time = event.start_time
                event.end_time = event.end_time
            else:
                event.start_time = ''
                event.end_time = ''
            event_list=[
                event.title,
                event.event_description,
                category,
                status,
                event.start_date,
                event.end_date,
                event.start_time if event.start_time else '',
                event.end_time if event.end_time else '',
                event.tkt_prize,
                event.ticket_site if event.ticket_site else '',
                event.tkt_phone if event.tkt_phone else '',
                event.event_website if event.event_website else '',
                event.facebook if event.facebook else '',
                event.googleplus if event.googleplus else '',
                event.contact_email if event.contact_email else '',
                event.phone if event.phone else '',
                listing_type, 
                event.listing_price if event.listing_price else '',
                event.listing_start if event.listing_start else '', 
                event.listing_end if event.listing_end else '',
                event.is_paid,
                event.seo_title, 
                event.seo_description, 
                tags
            ]
            venue_list=[
                venue.venue,  
                venue.address1,
                venue.address2,
                venue.type if venue.type else "",
                venue.telephone1,
                venue.mobile,
                venue.email,
                venue.website,
                venue.description if venue.description else "",
                venue.zip,
                venue.lat,
                venue.lon,
                venue.zoom,
                venue.seo_title,
                venue.seo_description,
            ] if venue else ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            event_list.extend(venue_list)
            event_list = [smart_unicode(text).encode('utf-8', 'ignore') for text in event_list]
            writer.writerow(event_list)
        return response
    else:
        data['categorys'] = EventCategory.objects.all().order_by('name')
        return render_to_response (template, data, context_instance=RequestContext(request))

def event_offline_payment(request, eid):
    template = 'payments/staff/process_offline_payment.html'
    obj = Event.objects.get(id=eid)
    ctype = ContentType.objects.get_for_model(obj)
    payobj = OfflinePayment.objects.get(
        content_type=ctype,
        object_id=obj.id,
        status='N'
    )
    data={
        'obj': obj,
        'payobj': payobj,
        'request_for': {'F': 'Featured Classified', 'S': 'Sponsored Classified'}[payobj.get_value('listing_type')],
        'submit_url': reverse('event_offline_payment', args=[obj.id]),
    }
    if request.method=='POST':
        option = request.POST['option']
        if option in ('AP', 'BD', 'BP'):
            payobj.processed_by = request.user
            payobj.approved_date = datetime.datetime.now()
            if option == 'AP':
                obj.status = payobj.status = 'P'
                obj.is_paid = True
                
                po = PaymentOrder(content_object=obj)
                po.invoice_no = get_invoice_num()
                po.payment_mode = 'Offline'
                po.status = 'Success'
                po.amount = obj.listing_price = payobj.amount
                po.user = obj.created_by
                po.object_name = obj.get_payment_title()
                po.phone_no = payobj.get_value('phone_no')
                po.email = payobj.get_value('email')
                po.offline_mode = request.POST.get('paytype')
                po.cheque_dd_num = request.POST.get('cheque_no')
                
                obj.listing_type = po.listing_type = payobj.get_value('listing_type')
                obj.payment = EventPrice.objects.get(level={'S': 'level1', 'F': 'level2'}[payobj.get_value('listing_type')])
                obj.listing_start = po.start_date = datetime.datetime.strptime(payobj.get_value('listing_start_date'), '%m/%d/%Y')
                obj.listing_end = po.end_date = datetime.datetime.strptime(payobj.get_value('listing_end_date'), '%m/%d/%Y')
                obj.listing_duration = (obj.listing_end - obj.listing_start).days
                datetime.datetime.now()
                
                po.save()
            elif option == 'BD':
                payobj.status = 'B' #Payment Rejected
                obj.status = 'D' #Object Drafted
            elif option == 'BP':
                payobj.status = 'B' #Payment Rejected
                obj.status = 'P' #Object Published
                
            obj.save() 
            payobj.save()
            
            if obj.status == 'P':
                try: mail_publish_event(obj)
                except: pass
            
            return HttpResponse(simplejson.dumps({'status':1}))
    return render_to_response(template,data,context_instance = RequestContext(request))
