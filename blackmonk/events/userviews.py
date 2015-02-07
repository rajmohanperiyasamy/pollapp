from datetime import date, timedelta
import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q, Count, Min, Max
from django.http import *
from django.shortcuts import render_to_response, get_list_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson, timezone
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.vary import vary_on_headers
import os
from random import sample
import re
from time import strptime
import time
import urllib
from xml.dom import minidom

from PIL import Image
from common import signals
from common.fileupload import upload_photos_forgallery, delete_photos
from common.getunique import getUniqueValue
from common.mail_utils import mail_publish_event
from common.models import ApprovalSettings, PaymentConfigure, Address
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name, get_status_class
from common.user_messages import EVENT_MSG
from common.utils import ds_pagination, get_lat_lng, get_global_settings, \
    ds_cleantext
from common.utilviews import crop_and_save_coverphoto
from events.forms import EventFormUser, UserEventSeoForm, UserVenueForm
from events.models import Event, EventCategory, Tag, EventPrice, EventRule, \
    EventOccurence
from events.utils import event_repeat_save, co_add_categories, co_add_tags
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from payments.models import PaymentOrder
from payments.utils import get_invoice_num, save_to_offline_payment


event_album_cat = PhotoCategory.objects.get_or_create(name="Events", slug='events', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
NO_OF_ITEMS_PER_PAGE=10

NO_OF_ITEMS_PER_PAGE = 10

status_dict = {
    'Rejected': 'R',
    'Draft': 'D',
    'Published': 'P',
    'Expired': 'E',
    'Pending': 'N',
    'Blocked': 'B',
}

@login_required
def dash_board(request,template='events/user/content_manager.html'):
    show = request.GET.get('show', None)
    eventcategory = EventCategory.objects.all().order_by('name')
    if show is None:
        eventsdisplay = Event.objects.filter(created_by=request.user).select_related('category','created_by').order_by('-created_on')
    else:
        eventsdisplay = Event.objects.filter(status=status_dict[show], created_by=request.user).select_related('category','created_by').order_by('-created_on')
    event_state = Event.objects.values('status').filter(created_by=request.user).annotate(s_count=Count('status'))
    
    msg = request.GET.get('msg',"")
    
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
    for st in event_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    page = request.REQUEST.get('page', '1')
    data = ds_pagination(eventsdisplay,page,'eventsdisplay',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    
    data['categorys'] = eventcategory
    data['total'] =total
    data['published'] =STATE['P']
    data['drafted'] =STATE['D']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['expired'] =STATE['E']
    data['search'] =False
    if show is not None:
        data['show'] = status_dict[show]
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def ajax_event_action(request,template='events/user/ajax_object_listing.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    action=request.GET['action']
    action_event = Event.objects.filter(id__in=id, created_by=request.user)
    
    if action=='DEL':
        for eve_del in action_event:
            signals.celery_delete_index.send(sender=None,object=eve_del)
            signals.create_notification.send(sender=None,user=request.user, obj=eve_del, not_type='deleted from',obj_title=eve_del.title)
            try:eve_del.album.delete()
            except:pass
        action_event.delete()
        msg=str(EVENT_MSG['EDS'])
        mtype=get_msg_class_name('s')
    else:pass
        
    data=filter_events(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['total']:send_data['total']=data['total']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype
    return HttpResponse(simplejson.dumps(send_data))

@login_required
def ajax_display_events(request,template='events/user/ajax_object_listing.html'):
    data=filter_events(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    return HttpResponse(simplejson.dumps(send_data))

def filter_events(request):
    data=key={}
    q=()
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    sort = request.GET.get('sort','-created_on')
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    
    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':key['listing_type'] = listing_type
    key['created_by'] = request.user
    
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        try:start_date = datetime.datetime(*strptime(request.GET['start_date'], "%d/%m/%Y")[0:5])
        except:
            start_date = False
        try:end_date = datetime.datetime(*strptime(request.GET['end_date'], "%d/%m/%Y")[0:5])
        except:
            end_date = False
        
        if search_category:
            key['category__id'] = search_category
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
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(venue__venue__icontains=search_keyword)|Q(venue__zip__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            eventsdisplay = Event.objects.filter(q,**key).select_related('category','created_by').order_by(sort)
        else:
            eventsdisplay = Event.objects.filter(**key).select_related('category','created_by').order_by(sort)
    else:
        eventsdisplay = Event.objects.filter(**key).select_related('category','created_by').order_by(sort)
    
    eventsdisplay = eventsdisplay.distinct()
    
    data = ds_pagination(eventsdisplay,page,'eventsdisplay',item_perpage)
    data['status'] = status
    if search:
        data['search_keyword'] = request.GET.get('kwd',"").strip()
    data['total'] = Event.objects.filter(created_by=request.user).count()
    data['listing_type'] = listing_type
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

@login_required
def ajax_event_state(request):
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
   
    event_state = Event.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in event_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'expired':STATE['E'],
    }
    return HttpResponse(simplejson.dumps(data))

@login_required
def add_event(request,template='events/user/event_form.html'):
    data={}
    try:
        eventobj = Event.objects.get( pk = request.REQUEST['eid'] )
        data['event'] = eventobj
        if request.method == 'POST':
            form = EventFormUser(request.POST,instance = eventobj)
            data['event_tags'] = request.POST['tags'].split(',')
            data['venue'] = Address.objects.get(id=request.POST['venue'])
        else:
            form = EventFormUser(instance = eventobj)
            data['event_tags']=eventobj.tags.all()
            data['venue'] = eventobj.venue
    except:
        eventobj = False
        if request.method == 'POST':
            form = EventFormUser(request.POST)
        else:
            form = EventFormUser()
    
    if request.method == 'POST':
        data['new_pic']=request.POST.getlist('new_pic')
        try:
            free_event = request.POST['free_event']
            if free_event:
                data['free_event_checked'] = 'checked'
        except:free_event = False
        if form.is_valid():
            sendsignal=False
            appreoval_settings = ApprovalSettings.objects.get(name='events')
            event=form.save(commit=False)
            event.slug=getUniqueValue(Event,slugify(event.title),instance_pk=event.id)
            event.created_by = request.user
            
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
            if not eventobj:
                event.status='D'
#                 if appreoval_settings.free:
#                     event.status='P'
#                 elif appreoval_settings.paid:
#                     event.status='P'
            else:
                if event.payment and event.status=='P':
                    if event.payment.level!='level0':
                        if appreoval_settings.paid_update or appreoval_settings.paid:
                            event.status='P'
                            try:mail_publish_event(event)
                            except:pass
                        else:event.status='N'
                    else:
                        if appreoval_settings.free_update or appreoval_settings.free:
                            event.status='P'
                            try:mail_publish_event(event)
                            except:pass
                        else:event.status='N'
                    sendsignal=True
            try:event.venue = Address.objects.get(id=request.POST['venue'])
            except:pass
            if free_event:
                event.tkt_prize = 'FREE'
            event.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=event)
            
            if "tags" in request.POST:
                co_add_tags(event,request.POST['tags'])
            co_add_categories(event, request.POST.getlist('category'))
            
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
                event.repeat_summary = None
                if event.rule and event.rule.id:
                    event.rule.delete() 
                    event.rule=None
                is_repeat = False
            try:event_occurence = EventOccurence.objects.filter(event = event).delete()
            except:pass
            if is_repeat: 
                rule,rslt,event = event_repeat_save(request,event,evnt_rule)
                rule.save()
                event.rule = rule
                for s in rslt:
                    event_occurence = EventOccurence()
                    event_occurence.date = s
                    event_occurence.event = event
                    event_occurence.save()
                     
            event.save()
            for log in event.audit_log.all():
                if log.action_type=='U':
                    log.delete()
            
            signals.celery_update_index.send(sender=None,object=event)
            if eventobj:
                if sendsignal:signals.create_staffmail.send(sender=None,object=event,module='events',action='U',user=request.user)
                signals.create_notification.send(sender=None,user=request.user, obj=eventobj, not_type='updated in',obj_title=eventobj.title)
                if eventobj.is_paid and eventobj.payment:
                    messages.success(request, str(EVENT_MSG['Wpus']))
                    return HttpResponseRedirect(reverse('events_dash_board'))
            else:
                signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=request.user)
                signals.create_notification.send(sender=None,user=request.user, obj=event, not_type='submitted in',obj_title=event.title)
            
            
            return HttpResponseRedirect(reverse('events_ajax_payment', args=(event.id,)))
        else:
            data['form'] = form
            data['eventobj']=eventobj
            return render_to_response(template ,data,context_instance=RequestContext(request))
    data['form'] = form
    return render_to_response(template,data,context_instance=RequestContext(request))


@login_required
def ajax_event_payment(request,id,template='events/user/listing_type.html'):
    try:
        request.GET['ajax']
        template='events/user/ajax_listing_type.html'
    except:
        pass
    data={}
    data['event'] = event = Event.objects.get(id=id,created_by=request.user)
    payment_settings = PaymentConfigure.get_payment_settings()
    data['event_price_objects'] = event_price_objects = EventPrice.objects.filter(level_visibility=True).order_by('id')
   
    if request.POST:
        level_selected = EventPrice.objects.get(level=request.POST['pricing'])
        appreoval_settings = ApprovalSettings.objects.get(name='events')
        lstart = datetime.datetime(*strptime(request.POST["listing_start_date"],"%m/%d/%Y")[0:5])
        lend = datetime.datetime(*strptime(request.POST["listing_end_date"],"%m/%d/%Y")[0:5])
        duration = (lend - lstart).days
        
        if level_selected.level == 'level2':
            sp_cost=level_selected.price*float(duration)
        elif level_selected.level == 'level1':
            sp_cost=level_selected.price
        else:
            sp_cost=0
            if appreoval_settings.free:
                event.status='P'
                try: mail_publish_event(event)
                except: pass
            else:
                event.status='N'
            event.listing_start = lstart
            event.listing_end = lend
            event.listing_duration = duration
            event.listing_type = 'B'
            event.listing_price = 0
            event.is_paid = True
            event.payment = level_selected
            event.save()
            
            for log in event.audit_log.all():
                if log.action_type=='U':
                    log.delete()
            
            ### Notification
            signals.celery_update_index.send(sender=None,object=event)
            notifictn_type = 'added as '+level_selected.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=event.created_by, obj=event, not_type=notifictn_type,obj_title=event.title)
            ### Notification
            messages.success(request, str(EVENT_MSG['WpMt']))
            return HttpResponseRedirect(reverse('events_dash_board'))
        
        payment_mode = request.POST.get('payment_mode%d'%(level_selected.id))
        
        if not payment_settings.online_payment or payment_mode == 'offline':
            save_to_offline_payment(
                object=event,
                listing_type={'level0': 'B', 'level1': 'S', 'level2': 'F'}[level_selected.level],
                amount=sp_cost,
                email=request.POST['email'],
                phone_no=request.POST['phone_no'],
                address=request.POST['address'],
                listing_start_date=request.POST['listing_start_date'],
                listing_end_date=request.POST['listing_end_date'],
            )
            event.status = 'N'
            event.save()
            
            for log in event.audit_log.all():
                if log.action_type=='U':
                    log.delete()
            messages.success(request, str(EVENT_MSG['WpMt']))
            return HttpResponseRedirect(reverse('events_dash_board'))
        else:
            if level_selected.level=='level2':
                listing_start = request.POST["listing_start_date"]
                listing_end = request.POST["listing_end_date"]
            else:
                listing_start=str(datetime.date.today().strftime('%m/%d/%Y'))
                listing_end=str(event.end_date.strftime('%m/%d/%Y'))
            return HttpResponseRedirect('/payments/events/confirm/'+str(event.id)+'/'+str(level_selected.id)+"?sdate="+listing_start+"&edate="+listing_end)
    data['today'] = timezone.now()
    data['payment_settings']=payment_settings
    return render_to_response(template,data,context_instance=RequestContext(request))

@login_required
def event_payment(request,template='events/user/event_payment.html'):
    data={}
    try:data['event']=event = Event.objects.get(id=request.GET['eid'])#,created_by=request.user,status='D')
    except:
        messages.error(request, str(EVENT_MSG['err']))
        return HttpResponseRedirect(reverse('events_dash_board'))
   
    payment_settings=PaymentConfigure.get_payment_settings()
    data['event_price_objects']=event_price_objects=EventPrice.objects.filter(level_visibility=True).order_by('id')
    if request.POST:
        try:
            level_selected = EventPrice.objects.get(level=request.POST['payment_level'])
            appreoval_settings = ApprovalSettings.objects.get(name='events')
        except:
            messages.error(request, str(EVENT_MSG['err']))
            return HttpResponseRedirect(reverse('events_dash_board'))
        
        sp_cost=0
        if level_selected.level!='level0':
            payment_mode=request.POST['payment_mode%d'%(level_selected.id)]
            if level_selected.level=='level2':
                lstart = datetime.datetime(*strptime(request.POST["fdsp_start_date"],"%Y/%m/%d")[0:5])
                lend = datetime.datetime(*strptime(request.POST["fdsp_end_date"],"%Y/%m/%d")[0:5])
                duration=lend-lstart
                duration=duration.days
                sp_cost=level_selected.price*float(duration)
            elif level_selected.level=='level1':sp_cost=level_selected.price
        else:
            if appreoval_settings.free:event.status='P'
            else:event.status='N'
            event.is_paid=False
            event.listing_price=sp_cost
            event.listing_type='B'
            event.payment=level_selected
            event.listing_start=datetime.datetime.now()
            event.listing_end=event.end_date
            event.save()
            ### Notification
            signals.celery_update_index.send(sender=None,object=event)
            notifictn_type = 'added as '+level_selected.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=event.created_by, obj=event, not_type=notifictn_type,obj_title=event.title)
            signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=request.user)
            ### Notification
            messages.success(request, str(EVENT_MSG['WpMt']))
            return HttpResponseRedirect(reverse('events_dash_board'))
        
        if not payment_settings.online_payment or payment_mode=='offline':
            event.payment = level_selected
            if level_selected.level=='level2':event.listing_type='F'
            elif level_selected.level=='level1':event.listing_type='S'
            elif level_selected.level=='level0':event.listing_type='B'
            event.payment=level_selected
            if level_selected.level=='level2':
                event.listing_start = datetime.datetime(*strptime(request.POST["fdsp_start_date"],"%Y/%m/%d")[0:5])
                event.listing_end = datetime.datetime(*strptime(request.POST["fdsp_end_date"],"%Y/%m/%d")[0:5])
                event.listing_duration=duration
            else:
                event.listing_start=datetime.datetime.now()
                event.listing_end=event.end_date
                event.listing_duration=duration
            event.status='N'
            event.is_paid=False
            event.listing_price=sp_cost
            event.save()
            ### Notification
            signals.celery_update_index.send(sender=None,object=event)
            notifictn_type = 'added as '+level_selected.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=event.created_by, obj=event, not_type=notifictn_type,obj_title=event.title)
            signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=request.user)
            ### Notification
            save_to_paymentorder(request,event,level_selected.level_label,sp_cost,event.listing_start,event.listing_end)
            messages.success(request, str(EVENT_MSG['WpMt']))
            return HttpResponseRedirect(reverse('events_dash_board'))
        
        else:
            if level_selected.level=='level2':
                listing_start = request.POST["fdsp_start_date"]
                listing_end = request.POST["fdsp_end_date"]
            else:
                listing_start=str(datetime.date.today())
                listing_end=str(event.end_date)
            return HttpResponseRedirect('/payments/events/confirm/'+str(event.id)+'/'+str(level_selected.id)+"?sdate="+listing_start+"&edate="+listing_end)
       
    else:
        data['payment_settings']=payment_settings
        return render_to_response(template,data,context_instance=RequestContext(request))
   

@login_required
def time_repeat(request,template='events/user/time_repeat.html'):
    data = {}
    ye = request.GET['edit']
    if ye == 'yes':
        data['edit']=True
        try:
            rule_id = request.GET['rule']
            repeated_val_occurence = EventRule.objects.get(id=rule_id)
            data['repeated_value'] = repeated_val_occurence.repeat_on_mnth
            data['repeat_option']= repeated_val_occurence.repeat
        except:
            pass
    else:data['edit']=False    
    try:""
    except:data['edit']=False    
    return render_to_response(template,data,context_instance=RequestContext(request))


@login_required
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
        try:
            event = Event.objects.get(id=request.GET['id'])
            album = event.album
            return upload_photos_forgallery(request,Photos,album,'album')
        except:
            return HttpResponse('No Object')


@login_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,EventPhoto,pk)

@login_required
def ajax_get_default_photos(request):  
    id=request.GET['ids']
    return get_default_images(request,id,EventPhoto)


@login_required
def ajax_add_venue(request,template='events/user/venue_form.html'):
    global_settings=get_global_settings()
    data={}
    try:
        venue = Address.objects.get(id=request.REQUEST['vid'])
        form = UserVenueForm(instance=venue)
    except:
        venue = False
        form = UserVenueForm()
    data['venue']=venue
    if request.method=='POST':
        if venue:
            form=UserVenueForm(request.POST,instance=venue)
        else:
            form=UserVenueForm(request.POST)
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
            template_name='events/user/part_address.html'
            return_data = {}
            return_data['venue'] = venue
            html=render_to_string(template_name,return_data, context_instance=RequestContext(request))
            send_data={'status':1,
                       'msg':str(EVENT_MSG['SAV']),
                       'mtype':get_msg_class_name('s'),
                       'address':address,
                       'id':venue.id ,
                       'html':html}
            return HttpResponse(simplejson.dumps(send_data))
        else:
            data['form']=form  
            return error_response(request,data,template,EVENT_MSG)  
    
    else:
        data['form']=form
    
    html = render_to_string(template, data, context_instance=RequestContext(request))
    send_data = {'status':1,'html':html}
    return HttpResponse(simplejson.dumps(send_data))


@login_required
def event_user_preview(request,id,template='events/user/preview.html'):
    data = {}
    try:
        event=Event.objects.get(id=id,created_by = request.user)
        data['event'] = event
    except:event=False 
    return render_to_response(template,data, context_instance=RequestContext(request))  


def auto_suggest(request):
    try:
        q = request.POST['query']
        data = Address.objects.filter(address_type = 'venue', venue__icontains = q)[:10]
    except:
        data = Address.objects.filter(address_type = 'venue')[:10]
    
    main=[]
    for ve in data:
       if  ve.zip:
           values=','.join([str(ve.venue), str(ve.address1),str(ve.zip)])
       else:
            values=','.join([str(ve.venue), str(ve.address1)]) 
       b={'id': ve.id, 'name': values, 'val': ve.id}
       main.append(b)
    return HttpResponse(simplejson.dumps(main), content_type="application/json")

def display_address(request):
    data = {}
    try:
        venue = Address.objects.get(id=request.GET['venue_id'])
        data['venue'] = venue
        template='events/user/part_address.html'
        html=render_to_string(template,data, context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({'status':1,'html':html}))
    except:
        venue = False
        data = {'status':0,'msg':str(EVENT_MSG['OOPS']),'mtype':get_msg_class_name('e')}
        return HttpResponse(simplejson.dumps(data))
    
@login_required
def seo(request,id,template='usercp_seo_form.html'):
    event = Event.objects.get(id = id)
    form=UserEventSeoForm(instance=event)
    if request.POST:
        form=UserEventSeoForm(request.POST,instance=event)
        if form.is_valid():
            seo=form.save(commit=False)
            seo.slug=slugify(seo.slug)
            seo.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(EVENT_MSG['ESUS'])}))
        else:
            data={'form':form,'event':event}
            return error_response(request,data,template,EVENT_MSG)
    data={'form':form,'event':event}
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required    
def save_to_paymentorder(request,event,event_type,featured_price,start_date,end_date):
    # THIS IS GOING TO BE CHANGED 
    return True
#     po=PaymentOrder(content_object = event)
#     po.invoice_no = get_invoice_num()
#     po.payment_mode = 'Offline'
#     po.status = 'Pending'
#     po.amount = featured_price
#     po.user = request.user
#     po.listing_type = event_type+' Event'
#     po.start_date=start_date
#     po.end_date=end_date
#     po.object_name=event.get_payment_title()
#     po.save()