from datetime import timedelta,date
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.html import strip_tags
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.core.mail import EmailMessage
from django.conf import settings as mysettings
from django.contrib import messages

from deal.forms import DealForm,DealSeoForm
from deal.models import Deal,DealCategory,DealPayment,Subscribe
from deal.utils import get_next_alpha

from common.imagehandling import *
from common.getunique import getUniqueValue,getSlugData
from common.templatetags.ds_utils import get_msg_class_name,get_status_class_custom
from common.staff_messages import DEAL_MSG,COMMON
from common.imagehandling import imageThumbnail,cropImage,db_thumbnail
from common.utils import ds_pagination, get_lat_lng
from common.utilviews import crop_and_save_coverphoto
from common.models import ModuleNames,Address
from business.models import Business,BusinessCategory,BusinessPrice
from business.forms import DealAddressForm,DealBusinessForm
from business.utils import co_add_categories
from common import signals

from gallery.models import PhotoAlbum, PhotoCategory, Photos
from common.fileupload import upload_photos_forgallery,delete_photos
deal_album_cat = PhotoCategory.objects.get_or_create(name="Deals", slug='deals', is_editable=False)[0]
from random import sample
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

#from common.forms import *
from common.utils import get_global_settings

from PIL import Image
import os
import random
import datetime
from time import strptime
import csv

NO_OF_ITEMS_PER_PAGE = 10
NO_OF_ITEMS_FEATURED = 300
User = get_user_model()

def set_soldout_expire():
    today = datetime.date.today()
    deals = Deal.objects.filter(status='P',end_date__lte=today)
    if deals:
        for deal in deals:
            deal.status = 'E'
            deal.save()

@staff_member_required
def list_deals(request,template='deal/staff/home.html'):
    categorys = DealCategory.objects.all().order_by('name')   
    deals = Deal.objects.all().order_by('-id')
    #set_soldout_expire()
    
    deals_state = Deal.objects.values('status').exclude(status='D').annotate(s_count=Count('status'))
    total = 0
    STATE={'B':0,'P':0,'E':0,'S':0,'N':0}
    for st in deals_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(deals,'1','deals',NO_OF_ITEMS_PER_PAGE)
    try:
        dl = Deal.objects.filter(status = 'P',featured = True)
        sum = dl.count()
        if sum >= NO_OF_ITEMS_FEATURED:
            data['feature_limit'] = True
    except:data['feature_limit'] = False  
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    
    data['category'] = categorys
    data['total'] =total
    data['inactive'] =STATE['B']
    data['active'] =STATE['P']
    data['expired'] =STATE['E']
    data['sold_out']=STATE['S']
    data['search'] =False
    
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def ajax_list_deals(request,template='deal/staff/ajax-deals-listing.html'):
    data=filter_deals(request)
    send_data={}
    try:
        dl = Deal.objects.filter(status = 'P',featured = True)
        sum = dl.count()
        if sum >= NO_OF_ITEMS_FEATURED:
            data['feature_limit'] = True
    except:data['feature_limit'] = False  
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
def ajax_deal_action(request,template='deal/staff/ajax_delete_listing.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    action_deal = Deal.objects.filter(id__in=id)
    cls_count=action_deal.count()
    status=0
    
    if action=='DEL':
        if request.user.has_perm('deal.delete_deal'):
            signals.celery_delete_indexs.send(sender=None,objects=action_deal)
            action_deal.delete()
            status=1
            msg=str(DEAL_MSG['SDD'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('deal.publish_deals'):
            action_deal.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=action_deal)
            status=1
            msg=str(DEAL_MSG[action])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
        
        
    data=filter_deals(request)
    
    new_id=[]
    for cs in data['deals']:new_id.append(int(cs.id))
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

def filter_deals(request):
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
    
    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':
        if listing_type =='F':key['featured'] = True
        else:key['featured'] = False
        
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:created_user = True
            
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        search_status = request.GET.get('srch_status',None)
        if search_category:
            categorys = DealCategory.objects.get(id=search_category)
            key['category'] = categorys
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='addr':
                key['address__address1__icontains'] = search_keyword
            else:key['created_by__display_name__icontains'] = search_keyword
        if search_status:
            key['status'] = search_status
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(address__address1__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if not created_user:deals = Deal.objects.filter(q,**key).select_related('category','created_by').order_by(sort)
            else:deals = Deal.objects.filter(q,**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if not created_user:deals = Deal.objects.filter(**key).select_related('category','created_by').order_by(sort)
            else:deals = Deal.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
                
    else:
        if not created_user: deals = Deal.objects.filter(**key).select_related('category','created_by').order_by(sort)
        else:deals = Deal.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
    
    data = ds_pagination(deals,page,'deals',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

@staff_member_required
def ajax_deal_state(request):
    status = request.GET.get('status','all')
    total = 0
    STATE={'B':0,'P':0,'E':0,'S':0,'N':0}
   
    if status == 'all':
        deal_state = Deal.objects.values('status').annotate(s_count=Count('status'))
    else:
        deal_state = Deal.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in deal_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'inactive':STATE['B'],
          'active':STATE['P'],
          'expired':STATE['E'],
          'sold_out':STATE['S'],
    }
    return HttpResponse(simplejson.dumps(data)) 

@staff_member_required
def add_deal(request,template='deal/staff/addDeal.html'):
    data = {}
    formdata = {}
    try:
        deal = Deal.objects.get(pk=request.REQUEST['did'])
        form = DealForm(instance=deal)
        if not request.user.has_perm('deal.change_deal'):
            raise PermissionDenied
        data['add'] = deal.address.all()[0]
    except:
        deal = False
        form = DealForm()
        if not request.user.has_perm('deal.add_deal'):raise PermissionDenied
    data['deal'] = deal
    flag=deal
    if request.method =='POST':
        if deal:
            form = DealForm(request.POST,request.FILES,instance=deal)
            newkey = False
        else:
            form = DealForm(request.POST,request.FILES)
            newkey = True
        try:
            add = Address.objects.get(id=request.POST['business'])
            data['add'] = add
        except:
            data['add'] = False
        data['new_pic']=request.POST.getlist('new_pic')    
        if form.is_valid():
            deal = form.save(commit=False)
            deal.slug=getUniqueValue(Deal,slugify(deal.title),instance_pk=deal.id)
            deal.created_by = request.user
            deal.modified_by = request.user
            if not deal.status == 'P':deal.status = 'B'
            
            if newkey:
                try:
                    d = Deal.objects.latest('id')
                    key = d.dealkey
                except:
                    key = 'AAA'    
                while True:
                    key = get_next_alpha(key)
                    try:
                        Deal.objects.get(dealkey=key)
                    except:
                        break
                deal.dealkey = key
                
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                if deal and deal.album:
                    album = deal.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = deal_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = deal.title
                album.slug = getUniqueValue(PhotoAlbum, slugify(deal.slug))
                album.seo_title = deal.title[:70],
                album.seo_description = album.summary = deal.about[:160]
                album.save()
                
                deal.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
            deal.seo_title = deal.title
            deal.seo_description = strip_tags(deal.about[:250])
            deal.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=deal)
            try:
                if request.POST['business']:
                    deal.address.clear()
                deal.address.add(Address.objects.get(id=request.POST['business']))
            except:
                pass
            subscript_deal_mail(request,deal)
            signals.celery_update_index.send(sender=None,object=deal)
            if 'did' in request.REQUEST:
                messages.success(request, str(DEAL_MSG['YUS']))
            else:
                messages.success(request, str(DEAL_MSG['YDS']))
            
            return HttpResponseRedirect(reverse('staff_deals_home'))
        else:
            data['form'] = form
    else:
        data['form'] = form   
    return render_to_response(template,data,context_instance=RequestContext(request))

@staff_member_required
def address_autosuggest(request):
    try:
        data = Address.objects.filter(Q(address1__icontains=request.GET['term'])&Q(address_type="business"))[:10]
    except:
        data = Address.objects.filter(address_type="business")[:10]
    main=[]
    for ve in data:
        address_label = ve.address1+', '+ve.city+'\n'+ve.zip
        b={'label':address_label,'id':str(ve.id)}
        main.append(b)
    return HttpResponse(simplejson.dumps(main))


@staff_member_required
def merchant_autosuggest(request):
    data = User.objects.filter(
        Q(useremail__icontains=request.GET['term'])|Q(display_name__icontains=request.GET['term'])
    )[:10]
    main = []
    for u in data:
        label = u.display_name + ' : ' + u.useremail
        b = {
            'label': label, 
            'id': str(u.id),
            'name': u.display_name.title(),
            'email': u.useremail
        }
        main.append(b)
    return HttpResponse(simplejson.dumps(main))


@staff_member_required
def add_address(request):
    data={}
    try:
        address_obj=Address.objects.get(id=request.REQUEST['id'])
        aform=DealAddressForm(instance=address_obj)
    except:
        address_obj=False
        aform=DealAddressForm()
    if request.method=='POST':
        if address_obj:
            aform=DealAddressForm(request.POST,instance=address_obj)
        else:
            aform=DealAddressForm(request.POST)    
        if aform.is_valid():
            global_settings = get_global_settings()
            address=aform.save(commit=False)
            address.created_by = request.user
            address.modified_by = request.user
            address.seo_title = None
            address.address_type="business"
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            address.save()
            template='deal/staff/ajax-address.html'
            html=render_to_string(template,{'add':address}, context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':1,'html':html}))
        else:
            try:
                data['lat'],data['lon'], zoom =  get_lat_lng(request.POST['lat_lng'])
                try:data['zoom'] = int(request.POST['zoom'])
                except:data['zoom'] = 15
            except:pass
            
            data['aform']=aform
            template='deal/staff/add_address.html'
            html=render_to_string(template,data,context_instance=RequestContext(request))
            send_data={'status':0,'html':html}
            return HttpResponse(simplejson.dumps(send_data))
    data['aform']=aform
    data['address']=address_obj
    template='deal/staff/add_address.html'     
    return render_to_response(template,data,context_instance=RequestContext(request))
    

@staff_member_required
def get_address(request):
    data = {}
    try:
        address = Address.objects.get(id=request.GET['bid'])
        data['add'] = address
        template='deal/staff/ajax-address.html'
        html=render_to_string(template,data, context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({'status':1,'html':html}))
    except:
        venue = False
        data = {'status':0,'msg':str(DEAL_MSG['OOPS']),'mtype':get_msg_class_name('e')}
        return HttpResponse(simplejson.dumps(data))
    

from common.fileupload import upload_photos,delete_photos,get_default_images

@staff_member_required
def ajax_upload_photos(request):
    if request.method == "POST":
        gal_id = request.POST.get('gal_id')
        if gal_id and gal_id.isdigit():
            album = PhotoAlbum.objects.get(id=gal_id)
        else:
            title = request.POST.get('title', "").strip()
            if not title:
                title = 'DealAlbum-' + "".join(sample(rand, 10))
            album = PhotoAlbum(
               created_by=request.user,
               title=title,
               slug=slugify(title),
               is_editable = False,
               category=deal_album_cat,
               seo_title=title[:70],
               summary=request.POST.get('about', title)[:2000],
               seo_description=request.POST.get('about', title)[:160]
            )
            album.save()
        response = upload_photos_forgallery(request,Photos,album,'album')
        album.save()
        return response
    else:
        try:
            deal = Deal.objects.get(id=request.GET['id'])
            album = deal.album
            return upload_photos_forgallery(request,Photos,album,'album')
        except:
            return HttpResponse('No Object')


@staff_member_required
def ajax_get_default_photos(request): 
    id=request.GET['ids']
    return get_default_images(request,id,DealPhotos)

@staff_member_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,DealPhotos,pk)

@staff_member_required
@permission_required('deal.change_deal',raise_exception=True)
def seo(request,id,template='deal/staff/update_seo.html'):
    deal = Deal.objects.get(id = id)
    form=DealSeoForm(instance=deal)
    if request.POST:
        form=DealSeoForm(request.POST,instance=deal)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug=slugify(seo.slug)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(DEAL_MSG['ASUS'])}))
        else:
            data={'form':form,'deal':deal}
            return error_response(request,data,template,DEAL_MSG)
    data={'form':form,'deal':deal}
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('deal.publish_deals',raise_exception=True)
def change_status(request):
    try:
        deal=Deal.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        deal.status = status
        deal.save()
        signals.celery_update_index.send(sender=None,object=deal)
        html ='<span title="'+get_status_class_custom(deal.status)+'" name="'+deal.status+'" id="id_estatus_'+str(deal.id)+'" class="inline-block status-idty icon-'+get_status_class_custom(deal.status)+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')
    
@staff_member_required
@permission_required('deal.promote_deals',raise_exception=True)
def feature_deal(request):
    try:
        deal=Deal.objects.get(id=int(request.GET['id']))
        featured = request.GET['status']
        if featured == 'F':
            deal.featured = True
        else:
            deal.featured = False    
        deal.save()
        return HttpResponse('1')
    except:return HttpResponse('0') 

@staff_member_required
def deal_preview(request,id,template='deal/staff/preview.html'):
    data = {}
    try:deal=Deal.objects.get(id=id)
    except:pass
    data['deal'] = deal
    return render_to_response(template,data, context_instance=RequestContext(request))    

@staff_member_required
def voucher_details(request,template='deal/staff/voucher-detail.html'):
    try:deal = Deal.objects.get(id=request.GET['did'])
    except:
        messages.error(request, str(DEAL_MSG['OOPS']))
        return HttpResponseRedirect(reverse('staff_deals_home'))
    data = {'deal':deal}
    data['deal_payments'] = DealPayment.objects.filter(deal = deal,status__in = '[S,D]').order_by('-id')
    return render_to_response(template,data,context_instance=RequestContext(request))

@staff_member_required
def subscript_deal_mail(request,deal):
    try:
        mails=Subscribe.objects.all()
        if mails:
            global_settings = get_global_settings()
            for sub in mails:    
                subject = global_settings.domain+' - Subscription for New Deal'
                subscript_community_mail_data = {}
                subscript_community_mail_data['from_name'] = global_settings.domain
                subscript_community_mail_data['subject'] = subject
                subscript_community_mail_data['sub'] = sub 
                email_message = render_to_string("deal/staff/subscript_mail.html",subscript_community_mail_data,context_instance=RequestContext(request))
                email= EmailMessage(subject,email_message, mysettings.DEFAULT_FROM_EMAIL,[sub.email])
                email.content_subtype = "html"
                email.send()
    except:
        pass