import Image
import ImageEnhance
import ImageFilter
from datetime import timedelta, date
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.html import strip_tags
from random import sample

from business.forms import UserBusinessForm, WorkingHoursForm, \
    UserBusinessSEOForm, ProductForm, CouponForm, EditUserBusinessForm, \
    UserAddressForm as AddressForm
from business.models import BusinessCategory, Attributes, AttributeValues, \
    BizAttributes, BusinessCoupons, BusinessProducts, BusinessPrice, \
    BusinessClaimSettings, WorkingHours, BusinessLogo, Business, Address, BusinessClaim
from business.utils import co_add_categories, save_to_claim_business, \
    co_add_tags
from common import signals
from common.fileupload import upload_photos_forgallery
from common.getunique import getUniqueValue, getSlugData
from common.mail_utils import mail_publish_business
from common.models import ApprovalSettings, PaymentConfigure
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name
from common.user_messages import BUSINESS_MSG
from common.utils import ds_pagination, get_lat_lng, ds_cleantext
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from payments.models import PaymentOrder
from payments.utils import get_invoice_num


business_album_cat = PhotoCategory.objects.get_or_create(name="Business", slug='business', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
PAY_MONTH_CHOICES = ((1, '1month'),(3, '3month'),(6, '6month'),(12, '1year'),)
NO_OF_ITEMS_PER_PAGE=10

status_dict = {
    'Rejected': 'R',
    'Draft': 'D',
    'Published': 'P',
    'Expired': 'E',
    'Pending': 'N',
    'Blocked': 'B',
}
######################################################################################################################
###########################################      BUSINESS      #######################################################
######################################################################################################################


@login_required
def manage_business(request,template='business/user/content_manager.html'):
    show = request.GET.get('show', None)
    claimed_biz_ids = BusinessClaim.objects.filter(user=request.user, is_paid=True).exclude(business__created_by=request.user).values_list('business', flat=True)
    if show is None:
        business = Business.objects.filter(
            Q(created_by=request.user)|Q(id__in=claimed_biz_ids)
        ).select_related('category').order_by('-created_on')
    else:
        business = Business.objects.filter(
            (Q(created_by=request.user)|Q(id__in=claimed_biz_ids))&Q(status=status_dict[show])
        ).select_related('category').order_by('-created_on')
    
    business_state = Business.objects.values('status').filter(
        Q(created_by=request.user)|Q(id__in=claimed_biz_ids)
    ).annotate(s_count=Count('status'))
    page = int(request.GET.get('page',1))
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    for st in business_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(business,page,'business',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =BUSINESS_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['categories'] = BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('parent_cat','name')
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['drafted'] =STATE['D']
    data['search'] =False
    if show is not None:
        data['show'] = status_dict[show]
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def ajax_business_state(request,template='business/user/ajax_sidebar.html'):
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    claimed_biz_ids = BusinessClaim.objects.filter(user=request.user, is_paid=True).exclude(business__created_by=request.user).values_list('business', flat=True)
    business_state = Business.objects.filter(
        Q(created_by=request.user)|Q(id__in=claimed_biz_ids)
    ).values('status').annotate(s_count=Count('status'))

    for st in business_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
        
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'drafted':STATE['D']
    }
    return HttpResponse(simplejson.dumps(data))

@login_required
def ajax_load_attribute(request):
    data={}
    try:cat=request.GET['cat_id'].split(',')
    except:cat=request.GET['cat_id']
    cat.append(request.GET['parent_cat_id'])
    cat=set(cat)
    attribute_group=Attributes.objects.filter(category_id__in=cat).order_by('attribute_group')
    data['attribute_group']=attribute_group
    category=BusinessCategory.objects.filter(id__in=cat).exclude(parent_cat__isnull=True)
    mpay=ypay=0
    for cat in category:
        if cat.price_month:mpay+=cat.price_month
        else:
            if cat.parent_cat.price_month:
                mpay+=cat.parent_cat.price_month

        if cat.price_year:ypay+=cat.price_year
        else:
            if cat.parent_cat.price_year:ypay+=cat.parent_cat.price_year
    try:
        business=Business.objects.get(id=int(request.GET['bid']))
        data['bizatr']=BizAttributes.objects.filter(business=business)
    except:pass
    #template = ['business/staff/update_attribute.html', 'business/user/update_attribute.html']["usercp" in request.GET]
    html=render_to_string('business/user/update_attribute.html', data, context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'html':html,'mpay':mpay,'ypay':ypay}))

@login_required
def ajax_list_business(request,template='business/user/ajax_object_listing.html'):
    data=filter(request)
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
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))


@login_required
def ajax_business_action(request,template='business/user/ajax_object_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    claimed_biz_ids = BusinessClaim.objects.filter(user=request.user, is_paid=True).exclude(business__created_by=request.user).values_list('business', flat=True)
    try:all_ids=request.GET['all_ids'].split(',')
    except:
        try:all_ids=request.GET['all_ids']
        except:all_ids=[]
    action=request.GET['action']
    business = Business.objects.filter(
        (Q(created_by=request.user)|Q(id__in=claimed_biz_ids))&Q(id__in=id)
    )
    
    if action=='DEL':
        for bus_del in business:
            signals.create_notification.send(sender=None,user=request.user, obj=bus_del, not_type='deleted from',obj_title=bus_del.name)
            signals.celery_delete_index.send(sender=None,object=bus_del)
            try:
                business_stripe_unsubscribe(bus_del.id)
                bus_del.album.delete()
            except:
                pass
        business.delete()
        msg=str(BUSINESS_MSG['BDS'])
        mtype=get_msg_class_name('s')
    else:
        business.update(status=action)
        signals.celery_update_indexs.send(sender=None,objects=business)
        msg=str(BUSINESS_MSG['BSCS'])
        mtype=get_msg_class_name('s')
    data=filter(request)
    new_id=[]
    
    for cs in data['business']:new_id.append(int(cs.id))
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagenation']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    send_data['total'] = Business.objects.filter(
        Q(created_by=request.user)|Q(id__in=claimed_biz_ids)
    ).count()
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))

   
def filter(request):
    data={}
    key={}
    args = q=()
    msg = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    sort = request.GET.get('sort','-created_on')
    
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
   
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    
    key['created_by'] = request.user
    
    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':key['featured_sponsored'] = listing_type
    
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        
        if search_category:
            categorys = BusinessCategory.objects.get(id=search_category)
            if categorys.parent_cat:
                key['categories'] = categorys
            else:
                key['categories__in'] = BusinessCategory.objects.filter(parent_cat=categorys)
        
        if search_type:
            if search_type=='title':key['name__icontains'] = search_keyword
            elif search_type=='description':key['description__icontains'] = search_keyword
        
        if search_keyword:
            q =(Q(name__icontains=search_keyword)|Q(categories__name__icontains=search_keyword)|Q(summary__icontains=search_keyword)|Q(description__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if len(args) == 0 :business = Business.objects.filter(q,**key).select_related('categories','created_by').order_by(sort)
            else:business = Business.objects.filter(q,**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :business = Business.objects.filter(**key).select_related('categories','created_by').order_by(sort)
            else:business = Business.objects.filter(**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :business = Business.objects.filter(**key).select_related('categories','created_by').order_by(sort)
        else:business = Business.objects.filter(args,**key).select_related('categories','created_by').order_by(sort)
    
    business=business.distinct()
    data = ds_pagination(business,page,'business',item_perpage)
    data['status'] = status
    if search:
        data['search_keyword'] = request.GET.get('kwd',"").strip()
    data['listing_type'] = listing_type
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

@login_required
def seo_business(request,id,template='usercp_seo_form.html'):
    business = Business.objects.get(id = id,created_by=request.user)
    form=UserBusinessSEOForm(instance=business)
    if request.POST:
        form=UserBusinessSEOForm(request.POST,instance=business)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(BUSINESS_MSG['BSUS'])}))
        else:
            data={'form':form,'business':business}
            return error_response(request,data,template,BUSINESS_MSG)
    data={'form':form,'business':business}
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def business_upgrade_listing_type(request,id,template='business/user/ajax_listing_type.html'):
    data={}
    payment_type=None
    business_obj = Business.objects.get(id = id,created_by=request.user)
    payment_settings=PaymentConfigure.get_payment_settings()
    if request.POST :
        try:
            business_price_obj = BusinessPrice.objects.get( level = request.POST['payment_level'])
            appreoval_settings = ApprovalSettings.objects.get(name='business')
        except:
            messages.error(request, str(BUSINESS_MSG['OOPS']))
            return HttpResponseRedirect(reverse('user_manage_business'))
        
        sp_cost=0
        if business_price_obj.level != 'level0':
            payment_mode=request.POST['payment_mode%d'%(business_price_obj.id)]
            payment_type=request.POST['payment_type']
            if not payment_settings.online_payment or payment_mode=='offline':
                business_obj.lstart_date=datetime.datetime.now()
                if payment_type == 'Y':business_obj.lend_date=date.today()+relativedelta(years=+1)
                else:business_obj.lend_date=date.today()+relativedelta(months=+1)
                business_obj.save()
            
            if payment_type=='M':
                if business_price_obj.level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_month:sp_cost=sp_cost+b_c.price_month
                        else:
                            if b_c.parent_cat.price_month:sp_cost=sp_cost+b_c.parent_cat.price_month
                elif business_price_obj.level=='level2':sp_cost=business_price_obj.price_month
                   
            elif payment_type=='Y': 
                 if business_price_obj.level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_year:sp_cost=sp_cost+b_c.price_year
                        else:
                            if b_c.parent_cat.price_year:sp_cost=sp_cost+b_c.parent_cat.price_year
                 elif business_price_obj.level=='level2':sp_cost=business_price_obj.price_year
        else:
            if appreoval_settings.free:
                business_obj.status='P'
                try:mail_publish_business(business_obj)
                except:pass
            else:business_obj.status='N'
            business_obj.lstart_date=datetime.datetime.now()
            business_obj.lend_date=date.today()+relativedelta(months=+1)
            business_obj.is_paid=False
            business_obj.sp_cost=sp_cost
            business_obj.featured_sponsored='B'
            business_obj.payment=business_price_obj
            business_obj.payment_type=payment_type
            business_obj.save()
            ### Notification
            signals.celery_update_index.send(sender=None,object=business_obj)
            notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=request.user, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)
            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=request.user)
            ### Notification
            messages.success(request, str(BUSINESS_MSG['BUS']))
            return HttpResponseRedirect(reverse('user_manage_business'))
        
        if not payment_settings.online_payment or payment_mode=='offline':
            business_obj.payment = business_price_obj
            if business_price_obj.level=='level2':business_obj.featured_sponsored='F'
            elif business_price_obj.level=='level1':business_obj.featured_sponsored='S'
            elif business_price_obj.level=='level0':business_obj.featured_sponsored='B'
            business_obj.payment=business_price_obj
            business_obj.payment_type=payment_type
            business_obj.status='N'
            business_obj.is_paid=False
            business_obj.sp_cost=sp_cost
            business_obj.save()
            ### Notification
            signals.celery_update_index.send(sender=None,object=business_obj)
            notifictn_type = 'upgraded to '+business_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=request.user, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)
            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=request.user)
            ### Notification
            save_to_paymentorder(request,business_obj,business_price_obj.level_label, business_obj.lstart_date, business_obj.lend_date)
            #messages.success(request, str(BUSINESS_MSG['BUS']))
            #return HttpResponseRedirect(reverse('user_manage_business'))
            if sp_cost > 0:
                return HttpResponseRedirect(reverse('business_payments_offline_confirm',args=[business_obj.id,business_price_obj.id])+'?type='+str(payment_type))
        else:
            if sp_cost > 0:
                return HttpResponseRedirect(reverse('business_payments_confirm',args=[business_obj.id,business_price_obj.id])+'?type='+str(payment_type))
        approval_settings=ApprovalSettings.objects.get(name='business')
        if sp_cost == 0:
            business_price_obj.level=='level0'
            business_obj.featured_sponsored ='B'
            if approval_settings.paid:
                business_obj.status='P'
                try:mail_publish_event(business_obj)
                except:pass
            else:business_obj.status='N'
            business_obj.save()
            return HttpResponseRedirect('/user/business/')
    data['business'] = business_obj
    try:
        for buz_cat in business_obj.categories.all():
            if buz_cat.parent_cat:
                cat=buz_cat.parent_cat
                break
        data['business_cat']=BusinessCategory.objects.filter(parent_cat=cat)
    except:pass
    s_monthly_price=s_yearly_price=0
    for b_c in business_obj.categories.all():
        if b_c.price_month:s_monthly_price=s_monthly_price+b_c.price_month
        else:
            if b_c.parent_cat.price_month:s_monthly_price=s_monthly_price+b_c.parent_cat.price_month
        
        if b_c.price_year:s_yearly_price=s_yearly_price+b_c.price_year
        else:
            if b_c.parent_cat.price_year:s_yearly_price=s_yearly_price+b_c.parent_cat.price_year
            
    data['s_monthly_price']=s_monthly_price
    data['s_yearly_price']=s_yearly_price
    
    data['business_price_objects'] = BusinessPrice.objects.filter(level_visibility=True).order_by('id')   
    data['payment_settings']=payment_settings
    return render_to_response(template,data,context_instance = RequestContext(request))

############################################# BUSINESS ADD ###############################################################

#@transaction.commit_on_success
@login_required
def add_business(request):
    category = BusinessCategory.objects.filter(parent_cat=None).order_by('name')
    date=datetime.datetime.now()
    formdata={'lstart_date':date,'lend_date':datetime.date.today()+relativedelta( months = +1 )}
    form= UserBusinessForm(initial=formdata)
    wform=WorkingHoursForm()
    aform=AddressForm()
    if request.POST:
        form = UserBusinessForm(request.POST)
        wform=WorkingHoursForm(request.POST)
        aform=AddressForm(request.POST)
        if form.is_valid() and wform.is_valid() and aform.is_valid():
            business = form.save(commit=False)
            business.created_by=business.modified_by=request.user
            business.is_claimable=False
            business.status='D'
            business.featured_sponsored='B'
            business.operating_hours=int(request.POST['operating_hours'])
            try:business.logo=BusinessLogo.objects.get(id=int(request.POST['new_pic']))
            except:pass
            business.slug = getUniqueValue(Business,slugify(getSlugData(request.POST['slug'])))
            business.created_by = business.modified_by = request.user
            business.save()
            
            seo_category = ''
            for category in business.categories.all():seo_category = seo_category+category.name+','
            business.seo_title = business.name
            business.seo_description = ds_cleantext(strip_tags(business.description[:250]))
            
            business.save()
            form.save_m2m()
            
            if business.operating_hours:
                workinghour=wform.save(commit=False)
                workinghour.status='P'
                workinghour.save()
                business.workinghours=workinghour
                business.save()
            
            for log in business.audit_log.all():
                if log.action_type=='U':
                    log.delete()
                    
            from common.utils import get_global_settings
            global_settings = get_global_settings()
            
            address=aform.save(commit=False)
            address.business=business
            address.status='P' 
            address.created_by = request.user
            address.modified_by = request.user
            address.seo_title = None
            address.venue = business.name
            address.address_type="business"
            address.slug=getUniqueValue(Address,slugify(business.name),instance_pk=address.id)
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            address.save()
            business.address.add(address)
            cat=request.POST.getlist('sub_category')
            cat.append(request.POST['category'])
            attribute=Attributes.objects.filter(category_id__in=cat).order_by('attribute_group').distinct()
           
            for attr in attribute:
                if attr.type == 'C':
                    atr=BizAttributes(business=business,key=attr)
                    atr.textbox_value=request.POST['attr_'+str(attr.id)]
                    atr.save()
                else:
                    try:
                        atr=BizAttributes.objects.get(business=business,key=attr)
                    except:
                        atr=BizAttributes(business=business,key=attr)
                        atr.save()
                    atr.value.clear()
                    for av in request.POST.getlist('attr_'+str(attr.id)):
                        atr.value.add(AttributeValues.objects.get(id=av))
                    
            
            co_add_tags(business,request.POST['tags'])
            co_add_categories(business, request.POST.getlist('sub_category'))
            transaction.commit()
            try:
                files=BusinessLogo.objects.filter(id=int(request.POST.getlist('new_files')))
                files.update(business=business)
            except:pass
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:
                if business.logo:
                    top = int(request.POST['logo_y1'])
                    left = int(request.POST['logo_x1'])
                    right = int(request.POST['logo_x2'])
                    bottom = int(request.POST['logo_y2'])
                    path = business.logo.logo.path
                    image = Image.open(path)
                    box = [ left, top, right, bottom ]
                    image = image.crop(box)
                    if image.mode not in ('L', 'RGB'):
                        image = image.convert('RGB')
                    enhancer = ImageEnhance.Sharpness(image)
                    image = enhancer.enhance(0.8)
                    image = image.filter(ImageFilter.DETAIL)
                    image.save(path,quality=90,optimised=True)
            except:
                pass
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            signals.celery_update_index.send(sender=None,object=business)
            try:
                request.POST['next']
                return HttpResponseRedirect(reverse('user_add_business_listing',args=[business.id]))
            except:
                messages.success(request, str(BUSINESS_MSG['BAS']))
                return HttpResponseRedirect(reverse('user_preview_business',args=[business.id]))
    data = { 'category': category, 'form':form}
    data['wform']=wform
    data['aform']=aform
    data['business_price_objects']=BusinessPrice.objects.filter(level_visibility=True).order_by('id')
    return render_to_response('business/user/business_form.html', data, context_instance=RequestContext(request))

@login_required
def add_business_listing(request,id):
    data={}
    payment_type=None
    try:business_obj = Business.objects.get(id = id,created_by=request.user)
    except:
        messages.error(request, str(BUSINESS_MSG['OOPS']))
        return HttpResponseRedirect(reverse('user_manage_business'))
    payment_settings=PaymentConfigure.get_payment_settings()
    if request.POST :
        try:
            business_price_obj = BusinessPrice.objects.get( level = request.POST['payment_level'])
            appreoval_settings = ApprovalSettings.objects.get(name='business')
        except:
            messages.error(request, str(BUSINESS_MSG['OOPS']))
            return HttpResponseRedirect(reverse('user_manage_business'))
        
        sp_cost=0
        if business_price_obj.level != 'level0':
            payment_mode=request.POST['payment_mode%d'%(business_price_obj.id)]
            payment_type=request.POST['payment_type']
            
            business_obj.lstart_date=datetime.datetime.now()
            if payment_type == 'Y':business_obj.lend_date=date.today()+relativedelta(years=+1)
            else:business_obj.lend_date=date.today()+relativedelta(months=+1)
            business_obj.save()
            
            for log in business_obj.audit_log.all():
                if log.action_type=='U':
                    log.delete()
                
            if payment_type=='M':
                if business_price_obj.level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_month:sp_cost=sp_cost+b_c.price_month
                        else:
                            if b_c.parent_cat.price_month:sp_cost=sp_cost+b_c.parent_cat.price_month
                elif business_price_obj.level=='level2':sp_cost=business_price_obj.price_month
                   
            elif payment_type=='Y': 
                if business_price_obj.level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_year:sp_cost=sp_cost+b_c.price_year
                        else:
                            if b_c.parent_cat.price_year:sp_cost=sp_cost+b_c.parent_cat.price_year
                elif business_price_obj.level=='level2':sp_cost=business_price_obj.price_year
            #business_obj.status='N'
        else:
            if appreoval_settings.free:
                business_obj.status='P'
                try:mail_publish_business(business_obj)
                except:pass
            else:business_obj.status='N'
            business_obj.lstart_date=datetime.datetime.now()
            business_obj.lend_date=date.today()+relativedelta(months=+1)
            business_obj.is_paid=False
            business_obj.sp_cost=sp_cost
            business_obj.featured_sponsored='B'
            business_obj.payment=business_price_obj
            business_obj.payment_type=payment_type
            business_obj.save()
            
            for log in business_obj.audit_log.all():
                if log.action_type=='U':
                    log.delete()
                
            ### Notification
            signals.celery_update_index.send(sender=None,object=business_obj)
            notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=request.user, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)
            if business_obj.status=='P' or business_obj.status=='N':
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=request.user)    
            ### Notification
            messages.success(request, str(BUSINESS_MSG['BAS']))
            return HttpResponseRedirect(reverse('user_manage_business'))
        
        if not payment_settings.online_payment or payment_mode=='offline':
            business_obj.payment = business_price_obj
            if business_price_obj.level=='level2':business_obj.featured_sponsored='F'
            elif business_price_obj.level=='level1':business_obj.featured_sponsored='S'
            elif business_price_obj.level=='level0':business_obj.featured_sponsored='B'
            business_obj.payment=business_price_obj
            business_obj.payment_type=payment_type
            business_obj.is_paid=False
            business_obj.sp_cost=sp_cost
            business_obj.save()
            
            for log in business_obj.audit_log.all():
                if log.action_type=='U':
                    log.delete()
                
            ### Notification
            signals.celery_update_index.send(sender=None,object=business_obj)
            notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=request.user, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)
            if business_obj.status=='P' or business_obj.status=='N':
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=request.user)### Notification
            save_to_paymentorder(request,business_obj,business_price_obj.level_label, business_obj.lstart_date, business_obj.lend_date)
            #messages.success(request, str(BUSINESS_MSG['BAS']))
            #return HttpResponseRedirect(reverse('user_manage_business'))
            if sp_cost > 0:
                return HttpResponseRedirect(reverse('business_payments_offline_confirm',args=[business_obj.id,business_price_obj.id])+'?type='+str(payment_type))
        
        if payment_settings.online_payment:
            business_obj.payment=business_price_obj
            business_obj.payment_type=payment_type
            business_obj.save()
            for log in business_obj.audit_log.all():
                if log.action_type=='U':
                    log.delete()
            if sp_cost > 0:
                return HttpResponseRedirect(reverse('business_payments_confirm',args=[business_obj.id,business_price_obj.id])+'?type='+str(payment_type))
            
        approval_settings=ApprovalSettings.objects.get(name='business')
        if sp_cost == 0:
            business_price_obj.level=='level0'
            business_obj.featured_sponsored ='B'
            if approval_settings.paid:
                business_obj.status='P'
                try:mail_publish_business(business_obj)
                except:pass
            else:business_obj.status='N'
            business_obj.save()
            return HttpResponseRedirect('/user/business/')
    data['business'] = business_obj
    try:
        for buz_cat in business_obj.categories.all():
            if buz_cat.parent_cat:
                cat=buz_cat.parent_cat
                break
        data['business_cat']=BusinessCategory.objects.filter(parent_cat=cat)
    except:pass
    s_monthly_price=s_yearly_price=0
    for b_c in business_obj.categories.all():
        if b_c.price_month:s_monthly_price=s_monthly_price+b_c.price_month
        else:
            if b_c.parent_cat.price_month:s_monthly_price=s_monthly_price+b_c.parent_cat.price_month
        
        if b_c.price_year:s_yearly_price=s_yearly_price+b_c.price_year
        else:
            if b_c.parent_cat.price_year:s_yearly_price=s_yearly_price+b_c.parent_cat.price_year
            
    data['s_monthly_price']=s_monthly_price
    data['s_yearly_price']=s_yearly_price
    
    data['business_price_objects'] = BusinessPrice.objects.filter(level_visibility=True).order_by('id')   
    data['payment_settings']=payment_settings
    return render_to_response('business/user/add_business_listing.html', data, context_instance=RequestContext(request))


@login_required
def ajax_upload_photos(request):
    if request.method == "POST":
        business = Business.objects.get(id=request.GET['id'])
        gal_id = request.POST.get('gal_id')
        if "id" in request.GET:
            if business.album:
                album = business.album
            else:
                title = request.POST.get('title', "").strip()
                if not title:
                    try:
                        title = business.name
                    except:
                        title = 'BusinessAlbum-' + "".join(sample(rand, 10))
                album = PhotoAlbum(
                   created_by=request.user,
                   title=title,
                   is_editable = False,
                   slug=slugify(title),
                   category=business_album_cat,
                   seo_title=title[:70],
                   status = 'N',
                   seo_description=request.POST.get('ebusiness_description', title)
                )
                album.save()
                business.album = album
                business.save()
        else:
            if gal_id and gal_id.isdigit():
                album = PhotoAlbum.objects.get(id=gal_id)
            else:
                title = request.POST.get('title', "").strip()
                if not title:
                    try:
                        title = business.name
                    except:
                        title = 'BusinessAlbum-' + "".join(sample(rand, 10))
                album = PhotoAlbum(
                   created_by=request.user,
                   title=title,
                   is_editable = False,
                   category=business_album_cat,
                   seo_title=title[:70],
                   status = 'N',
                   seo_description=request.POST.get('ebusiness_description', title)
                )
                album.save()
                business.album = album
                business.save()
        response = upload_photos_forgallery(request,Photos,album,'album')
        album.save()
        return response
    else:
        business = Business.objects.get(id=request.GET['id'])
        album = business.album
        return upload_photos_forgallery(request,Photos,album,'album')


@login_required
def claim_business(request,id):
    data={}
    payment_type=None
    claim = BusinessClaimSettings.get_setting()
    business_obj = Business.objects.get(id = id,is_claimable=True)
#     try:
#     except:
#         messages.error(request, str(BUSINESS_MSG['OOPS']))
#         return HttpResponseRedirect(reverse('user_manage_business'))
    
#     if not claim.allow_claim or not claim.allow_free_buz_claim:
#         if not business_obj.created_by.is_staff :
#             messages.error(request, str(BUSINESS_MSG['OOPS']))
#             return HttpResponseRedirect(reverse('user_manage_business'))
#     if not claim.allow_free_buz_claim and business_obj.featured_sponsored == 'B':
#         messages.error(request, str(BUSINESS_MSG['OOPS']))
#         return HttpResponseRedirect(reverse('user_manage_business'))
    
    payment_settings=PaymentConfigure.get_payment_settings()
    if request.POST :
        appreoval_settings = ApprovalSettings.objects.get(name='business')
        
        level = request.POST['payment_level']
        payment_type = request.POST['payment_type']
        business_price_obj = BusinessPrice.objects.get(level=level)
        payment_mode = request.POST['payment_mode%d'%(business_price_obj.id)]
        
        business_obj.payment = business_price_obj
        business_obj.payment_type = payment_type
        business_obj.save()
        sp_cost=0
        if level != 'level0':
            business_obj.lstart_date=datetime.datetime.now()
            if payment_type=='M':
                if level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_month:
                            sp_cost=sp_cost+b_c.price_month
                        else:
                            if b_c.parent_cat.price_month:
                                sp_cost=sp_cost+b_c.parent_cat.price_month
                elif level=='level2':
                    sp_cost = business_price_obj.price_month
                   
            elif payment_type=='Y': 
                 if level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_year:
                            sp_cost=sp_cost+b_c.price_year
                        else:
                            if b_c.parent_cat.price_year:
                                sp_cost=sp_cost+b_c.parent_cat.price_year
                 elif level=='level2':
                     sp_cost = business_price_obj.price_year
            business_obj.sp_cost = sp_cost
            business_obj.save()
            save_to_claim_business(request.user, business_obj, level=level)
        else:
            business_obj.lstart_date=datetime.datetime.now()
            business_obj.lend_date=date.today()+relativedelta(months=+1)
            business_obj.featured_sponsored = 'B'
            business_obj.sp_cost = sp_cost
            business_obj.save()
            
            signals.celery_update_index.send(sender=None,object=business_obj)
            if ( claim.auto_aprove_paid_buz_claim and business_obj.featured_sponsored in ['F', 'S'] ) or \
                ( claim.auto_aprove_free_buz_claim and business_obj.featured_sponsored == 'B' ):
                save_to_claim_business(request.user, business_obj, approve=True, paid=True, level=level)
            else:
                save_to_claim_business(request.user, business_obj, paid=True, level=level)
            signals.create_notification.send(sender=None,user=request.user, obj=business_obj, not_type='claimed in',obj_title=business_obj.name)
            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=request.user)
            messages.success(request, str(BUSINESS_MSG['BUS']))
            return HttpResponseRedirect(reverse('user_manage_business'))
        
        if not payment_settings.online_payment or payment_mode=='offline':
            signals.celery_update_index.send(sender=None,object=business_obj)
            save_to_paymentorder(request,business_obj,business_price_obj.level_label, business_obj.lstart_date, business_obj.lend_date)
            if ( claim.auto_aprove_paid_buz_claim and business_obj.featured_sponsored in ['F', 'S'] ) or \
                ( claim.auto_aprove_free_buz_claim and business_obj.featured_sponsored == 'B' ):
                save_to_claim_business(request.user, business_obj, approve=True, paid=True, level=level)
            else:
                save_to_claim_business(request.user, business_obj, paid=True, level=level)
            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=request.user)
            signals.create_notification.send(sender=None,user=request.user, obj=business_obj, not_type='claimed in',obj_title=business_obj.name)
            return HttpResponseRedirect(reverse('business_payments_offline_confirm',args=[business_obj.id,business_price_obj.id])+'?type='+str(payment_type))
        else:
            return HttpResponseRedirect(reverse('business_payments_confirm',args=[business_obj.id,business_price_obj.id])+'?type='+str(payment_type)+'&c=1')
        
    data['business'] = business_obj
    try:
        for buz_cat in business_obj.categories.all():
            if buz_cat.parent_cat:
                cat=buz_cat.parent_cat
                break
        data['business_cat']=BusinessCategory.objects.filter(parent_cat=cat)
    except:pass
    s_monthly_price = s_yearly_price = 0
    for b_c in business_obj.categories.all():
        if b_c.price_month:
            s_monthly_price=s_monthly_price+b_c.price_month
        else:
            if b_c.parent_cat.price_month:
                s_monthly_price=s_monthly_price+b_c.parent_cat.price_month
        
        if b_c.price_year:
            s_yearly_price=s_yearly_price+b_c.price_year
        else:
            if b_c.parent_cat.price_year:
                s_yearly_price=s_yearly_price+b_c.parent_cat.price_year
            
    data['s_monthly_price']=s_monthly_price
    data['s_yearly_price']=s_yearly_price
    
    data['business_price_objects'] = BusinessPrice.objects.filter(level_visibility=True).order_by('id')   
    data['payment_settings']=payment_settings
    return render_to_response('business/user/claim_business.html', data, context_instance=RequestContext(request))


@login_required
def update_business(request,id):
    business=Business.objects.get(id=id,created_by=request.user)
    try:whour=WorkingHours.objects.get(id=business.workinghours.id)
    except:whour=None
    try:address=Address.objects.get(business=business,status='P')
    except:address=None
    try:albumid = business.album_id
    except:albumid = None
    form= EditUserBusinessForm(instance=business)
    wform=WorkingHoursForm(instance=whour)
    aform=AddressForm(instance=address)
    if request.method=='POST':
        form = EditUserBusinessForm(request.POST,instance=business)
        wform=WorkingHoursForm(request.POST,instance=whour)
        aform=AddressForm(request.POST,instance=address)
        if form.is_valid() and wform.is_valid() and aform.is_valid():
            appreoval_settings = ApprovalSettings.objects.get(name='business')
            business = form.save(commit=False)
            business.modified_by=request.user
            if business.status=='P':
                sendsignal=True
            else:
                sendsignal=False
            if business.payment and business.status=='P':
                if business.payment.level != 'level0':
                    if appreoval_settings.paid_update:
                        business.status='P'
                        try:mail_publish_business(business)
                        except:pass
                    else:
                        business.status='N'
                else:
                    if appreoval_settings.free_update:
                        business.status='P'
                        try:mail_publish_business(business)
                        except:pass
                    else:
                        business.status='N'
            
            business.operating_hours=int(request.POST['operating_hours'])
            try:business.logo=BusinessLogo.objects.get(id=int(request.POST['new_pic']))
            except:pass
            business.slug = getUniqueValue(Business,slugify(getSlugData(request.POST['slug'])),instance_pk=business.id)
            business.modified_by = request.user
            business.album_id = albumid

            for log in business.audit_log.all()[:1]:
                if log.action_type=='U':
                    log.delete()
            
            business.save()
            
            form.save_m2m()
            if business.operating_hours:
                workinghour=wform.save(commit=False)
                workinghour.status='P'
                workinghour.save()
                business.workinghours=workinghour
                business.save()
                for log in business.audit_log.all()[:1]:
                    if log.action_type=='U':
                        log.delete()
                
           
            
            from common.utils import get_global_settings
            global_settings = get_global_settings()
            
            address=aform.save(commit=False)
            address.business=business
            address.status='P' 
            address.created_by = request.user
            address.modified_by = request.user
            address.seo_title = None
            address.venue = business.name
            address.address_type="business"
            address.slug=getUniqueValue(Address,slugify(business.name),instance_pk=address.id)
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            address.save()
            business.address.add(address)
            cat=request.POST.getlist('sub_category')
            cat.append(request.POST['category'])
            attribute=Attributes.objects.filter(category_id__in=cat).order_by('attribute_group').distinct()
            
            
            claer_atr=BizAttributes.objects.filter(business=business)
            claer_atr.delete()
            for attr in attribute:
                if attr.type == 'C':
                    try:
                        atr=BizAttributes.objects.get(business=business,key=attr)
                        atr.textbox_value=request.POST['attr_'+str(attr.id)]
                        atr.save()
                    except:
                        atr=BizAttributes(business=business,key=attr)
                        atr.textbox_value=request.POST['attr_'+str(attr.id)]
                        atr.save()
                else:
                    try:
                        atr=BizAttributes.objects.get(business=business,key=attr)
                    except:
                        atr=BizAttributes(business=business,key=attr)
                        atr.save()
                    atr.value.clear()
                    for av in request.POST.getlist('attr_'+str(attr.id)):
                        atr.value.add(AttributeValues.objects.get(id=av))
            
            co_add_tags(business,request.POST['tags'])
            co_add_categories(business, request.POST.getlist('sub_category'))
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            try:
                if business.logo:
                    top = int(request.POST['logo_y1'])
                    left = int(request.POST['logo_x1'])
                    right = int(request.POST['logo_x2'])
                    bottom = int(request.POST['logo_y2'])
                    path = business.logo.logo.path
                    image = Image.open(path)
                    box = [ left, top, right, bottom ]
                    image = image.crop(box)
                    if image.mode not in ('L', 'RGB'):
                        image = image.convert('RGB')
                    enhancer = ImageEnhance.Sharpness(image)
                    image = enhancer.enhance(0.8)
                    image = image.filter(ImageFilter.DETAIL)
                    image.save(path,quality=90,optimised=True)
            except:
                pass
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if business.is_paid and business.sp_cost:
                signals.create_notification.send(sender=None,user=request.user, obj=business, not_type='updated in',obj_title=business.name)
                signals.celery_update_index.send(sender=None,object=business)
                if sendsignal:
                    signals.create_staffmail.send(sender=None,object=business,module='business',action='U',user=request.user)
                messages.success(request, str(BUSINESS_MSG['BUS']))
                return HttpResponseRedirect(reverse('user_preview_business',args=[business.id]))
            else:
                return HttpResponseRedirect(reverse('user_add_business_listing',args=[business.id]))
    business_tags=business.tags.all()
    category = BusinessCategory.objects.filter(parent_cat=None).order_by('name')
    data = { 'category': category, 'form':form,'business':business,'address':address,'slug':business.slug,  'business_tags':business_tags}
    data['wform']=wform
    data['aform']=aform
    cat_id=[]
    for c in business.categories.all():
        cat_id.append(c.id)
        try:cat_id.append(c.parent_cat.id)
        except:pass
    cat_id=set(cat_id)
    attribute_group=Attributes.objects.filter(category_id__in=cat_id).order_by('attribute_group')
    data['attribute_group']=attribute_group
    data['bizatr']=BizAttributes.objects.filter(business=business)
    for bcat in business.categories.all():
        if bcat.parent_cat:data['parent_cat']=bcat.parent_cat
    return render_to_response('business/user/update_business.html', data, context_instance=RequestContext(request))

"""
##################################################################################################################
#######################################    PREVIEW PRODUCT COUPON IMAGE     ######################################
##################################################################################################################
"""
@login_required
def preview_business(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id,created_by=request.user)
    data['usr_editable'] = True
    try:data['msg'] =BUSINESS_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    try:view = request.GET['view']
    except: view = 'home'
    
    if view=='photos':
        if business.payment.images=='Y':view=='photos'
        else:view = 'home'
    elif view=='products':
        if business.payment.product=='Y':
            view=='products'
            try:
                data['bproduct'] = BusinessProducts.objects.get(business=business,id=int(request.GET['pid']))
                data['view_product']=int(request.GET['pid'])
            except:pass
        else:view = 'home'
    elif view=='coupons':
        if business.payment.offer_coupon=='Y':
            view=='coupons'
            try:
                data['bcoupons'] = BusinessCoupons.objects.get(business=business,type='C',id=int(request.GET['cid']))
                data['view_coupon']=int(request.GET['cid'])
            except:pass
        else:view = 'home'
    elif view=='offers':
        if business.payment.offer_coupon=='Y':
            view=='offers'
            try:
                data['boffer'] = BusinessCoupons.objects.get(business=business,id=int(request.GET['oid']))
                data['view_offer']=int(request.GET['oid'])
            except:pass
        else:view = 'home'
    else:
        if not view!='comments':view=='home'
    try:
        if business.payment.offer_coupon=='Y':
            data['offers'] = BusinessCoupons.objects.filter(business=business, end_date__gte=date.today())
            data['coupons'] = BusinessCoupons.objects.filter(business=business,type='C',end_date__gte=date.today())
    except:
        data['offers'] = None
        data['coupons'] = None
    data['preview']='preview'
    data['view']=view
    data['claim']=BusinessClaimSettings.get_setting()
    data['today'] = date.today()
    return render_to_response('business/user/preview.html',data,context_instance=RequestContext(request)) 

@login_required
def business_images(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id,created_by=request.user)
    return render_to_response('business/user/images.html',data,context_instance=RequestContext(request)) 

@login_required
def business_product(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id,created_by=request.user)
    data['products']=BusinessProducts.objects.filter(business=business).order_by('-created_on')
    return render_to_response('business/user/product.html',data,context_instance=RequestContext(request)) 

@login_required
def business_update_product(request,bid,id=None):
    data={}
    data['business'] = {'id':bid}
    if id is not None:
        data['product'] = product = BusinessProducts.objects.get(id=id)
        form = ProductForm(instance=product)
    else:
        form = ProductForm()
    if request.method == 'POST':
        if id:
            form = ProductForm(request.POST,instance=product)
        else:
            form = ProductForm(request.POST)
        if form.is_valid():
            business = Business.objects.get(id=bid,created_by=request.user)
            product = form.save(commit=False)
            product.business = business
            product.description = product.description[:1000]
            product.is_active = True
            product.created_by = request.user
            product.save()
            if product.photo:
                image_url = product.photo.url
            else:
                image_url = "/static/themes/img/no-image.png"
            html=render_to_string('business/user/load_product.html',{'product':product,'business':product.business},context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':1,'image_url':image_url,'html':html,'title':product.title,'description':product.description,'id':product.id,'msg':str(BUSINESS_MSG['BPUS']),'mtype':get_msg_class_name('s')}))
        else:
            data['form'] = form
            html = render_to_string('business/user/update_product.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    data['form'] = form
    return render_to_response('business/user/update_product.html',data,context_instance=RequestContext(request))

@login_required
def business_delete_product(request):
    try:
        product=BusinessProducts.objects.get(id=int(request.POST['id']))
        product.delete()
        return HttpResponse(simplejson.dumps({'status':1,'msg':str(BUSINESS_MSG['BPDS']),'mtype':get_msg_class_name('s')}))
    except:return HttpResponse(simplejson.dumps({'status':0,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

# @login_required
# def business_product_load_html(request):
#     try:
#         product=BusinessProducts.objects.get(id=int(request.POST['id']))
#         html=render_to_string('business/user/load_product.html',{'product':product,'business':product.business},context_instance=RequestContext(request))
#         return HttpResponse(simplejson.dumps({'html':html,'status':1}))
#     except:return HttpResponse(simplejson.dumps({'status':0}))
############################################################################################################
############################################################################################################
############################################################################################################
@login_required
def business_coupon(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id,created_by=request.user)
    data['coupons']=BusinessCoupons.objects.filter(business=business)
    return render_to_response('business/user/coupon.html',data,context_instance=RequestContext(request)) 

@login_required
def business_update_coupon(request,bid,id=None):
    data={}
    data['business'] = {'id': bid}
    if id is not None:
        data['coupon']=coupon=BusinessCoupons.objects.get(id=id)
        form=CouponForm(instance=coupon)
    else:
        form=CouponForm()
    if request.method=='POST':
        if id:form=CouponForm(request.POST,instance=coupon)
        else:form=CouponForm(request.POST)
        if form.is_valid():
            business= Business.objects.get(id=bid,created_by=request.user)
            coupon=form.save(commit=False)
            coupon.business=business
            coupon.is_active=True
            coupon.created_by=request.user
            coupon.save()
            if coupon.photo:
                image_url = coupon.photo.url
            else:
                image_url = "/static/themes/img/no-image.png"
            html=render_to_string('business/user/load_coupon.html',{'coupon':coupon,'business':coupon.business},context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':1,'image_url':image_url,'str_date':coupon.start_date.strftime('%B %d, %Y'),'end_date':coupon.end_date.strftime('%B %d, %Y'),'title':coupon.title,'description':coupon.description,'html': html,'id':coupon.id,'msg':str(BUSINESS_MSG['BCUS']),'mtype':get_msg_class_name('s')}))
        else:
            data['form']=form
            html=render_to_string('business/user/update_coupon.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    data['form']=form
    return render_to_response('business/user/update_coupon.html',data,context_instance=RequestContext(request))

@login_required
def business_delete_coupon(request):
    try:
        product=BusinessCoupons.objects.get(id=int(request.POST['id']))
        product.delete()
        return HttpResponse(simplejson.dumps({'status':1,'msg':str(BUSINESS_MSG['BCDS']),'mtype':get_msg_class_name('s')}))
    except:return HttpResponse(simplejson.dumps({'status':0,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

# @login_required
# def business_coupon_load_html(request):
#     try:
#         coupon=BusinessCoupons.objects.get(id=int(request.POST['id']))
#         html=render_to_string('business/user/load_coupon.html',{'coupon':coupon,'business':coupon.business},context_instance=RequestContext(request))
#         return HttpResponse(simplejson.dumps({'html':html,'status':1}))
#     except:
#         return HttpResponse(simplejson.dumps({'status':0}))
############################################################################################################
############################################################################################################
############################################################################################################
@login_required
def business_address(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id,created_by=request.user)
    data['buz_address']=Address.objects.filter(business=business)
    return render_to_response('business/user/address.html',data,context_instance=RequestContext(request)) 

@login_required
def business_update_address(request,bid,id=None):
    data={}
    data['business']=business= Business.objects.get(id=bid,created_by=request.user)
    if id:
        data['address']=address=Address.objects.get(id=id)
        form=AddressForm(instance=address)
    else:form=AddressForm()
    if request.method=='POST':
        if id:form=AddressForm(request.POST,instance=address)
        else:form=AddressForm(request.POST)
        if form.is_valid():
            from common.utils import get_global_settings
            global_settings = get_global_settings()
            
            address=form.save(commit=False)
            address.business=business
            address.status='P' 
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            address.save()
            return HttpResponse(simplejson.dumps({'status':1,'id':address.id,'msg':str(BUSINESS_MSG['BAUS']),'mtype':get_msg_class_name('s')}))
        else:
            data['form']=form
            html=render_to_string('business/user/update_address.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    data['form']=form
    return render_to_response('business/user/update_address.html',data,context_instance=RequestContext(request))

@login_required
def business_delete_address(request):
    try:
        address=Address.objects.get(id=int(request.POST['id']),created_by=request.user)
        address.delete()
        return HttpResponse(simplejson.dumps({'status':1,'msg':str(BUSINESS_MSG['BADS']),'mtype':get_msg_class_name('s')}))
    except:return HttpResponse(simplejson.dumps({'status':0,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

@login_required
def save_to_paymentorder(request,business,business_type,start_date,end_date):
    po=PaymentOrder(content_object = business)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Pending'
    po.amount = business.sp_cost
    po.user = request.user
    po.listing_type = str(business_type)+' Business'
    po.start_date=start_date
    po.end_date=end_date 
    po.object_name=business.get_payment_title()
    po.save()
    return True

@login_required
def ajax_listing_add_cat(request):
    data={}
    id=request.GET['id']
    cat=BusinessCategory.objects.get(id=int(request.GET['cid']))
    try:
        business=Business.objects.get(id=int(request.GET['bid']),created_by=request.user)
    except:
        business=Business.objects.get(id=int(request.GET['bid']),is_claimable=True)
    try:
        try:
            check_cat=business.categories.get(id=cat.id)
            if check_cat:return HttpResponse('1')
        except:pass
        business.categories.add(cat)
        s_monthly_price=s_yearly_price=0
        for b_c in business.categories.all():
            if b_c.price_month:s_monthly_price=s_monthly_price+b_c.price_month
            else:
                if b_c.parent_cat.price_month:s_monthly_price=s_monthly_price+b_c.parent_cat.price_month
            
            if b_c.price_year:s_yearly_price=s_yearly_price+b_c.price_year
            else:
                if b_c.parent_cat.price_year:s_yearly_price=s_yearly_price+b_c.parent_cat.price_year
        
        currency=PaymentConfigure.get_payment_settings().currency_symbol
        data['t_month']= str(s_monthly_price) +str(currency)
        data['t_year']=str(s_yearly_price) +str(currency)
        yprice=mprice=0
        if cat.price_month: mprice=cat.price_month
        else:
            if cat.parent_cat.price_month:mprice=cat.parent_cat.price_month
        if cat.price_year:yprice=cat.price_year
        else:
            if cat.parent_cat.price_year:yprice=cat.parent_cat.price_year
         
        
        #data['month']="<tr id='mcat"+str(cat.id)+"'><td style='width:250px;'>"+str(cat)+"</td><td style='width:90px;'>"+ str(currency) +str(mprice)+"</td><td><a style='float:right;' href='javascript:remove_cat("+str(cat.id)+","+str(id)+")'>X</a></tr>"
        mids="mcat"+str(cat.id)
        data['month']="<li style='font-size: 14px; font-weight: bold; color: rgb(85, 85, 85);' id='"+mids+"'>"+str(cat)+" <strong style='color: rgb(0, 0, 0);'>"
        data['month']+=str(currency) +str(mprice)+"</strong>"
        data['month']+="<span class='pLrT' onclick='remove_cat("+str(cat.id)+","+str(id)+")'><i aria-hidden='true' class='bUi-iCn-rMv-12 cLr-gRy fS9' style=' cursor: pointer;'></i></span></li>"
        #data['year']="<tr id='ycat"+str(cat.id)+"'><td style='width:250px;'>"+str(cat)+"</td><td style='width:90px;'>"+ str(currency) +str(yprice)+"</td><td><a style='float:right;' href='javascript:remove_cat("+str(cat.id)+","+str(id)+")'>X</a></tr"
        yids="ycat"+str(cat.id)
        data['year']="<li style='font-size: 14px; font-weight: bold; color: rgb(85, 85, 85);' id='"+yids+"'>"+str(cat)+" <strong style='color: rgb(0, 0, 0);'>"
        data['year']+=str(currency) +str(yprice)+"</strong>"
        data['year']+="<span class='pLrT' onclick='remove_cat("+str(cat.id)+","+str(id)+")'><i aria-hidden='true' class='bUi-iCn-rMv-12 cLr-gRy fS9' style=' cursor: pointer;'></i></span></li>"
    except:
        data={}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@login_required
def ajax_listing_delete_cat(request):
    data={}
    id=request.GET['id']
    cat=BusinessCategory.objects.get(id=int(request.GET['cid']))
    try:
        business=Business.objects.get(id=int(request.GET['bid']),created_by=request.user)
    except:
        business=Business.objects.get(id=int(request.GET['bid']),is_claimable=True)
    try:
        if business.categories.all().count() == 1:
            return HttpResponse('1')
        business.categories.remove(cat)
        try:
            attr=Attributes.objects.filter(category=cat)
            bizattr=BizAttributes.objects.filter(key__in=attr,business=business)
            bizattr.delete()
        except:pass
        s_monthly_price=s_yearly_price=0
        for b_c in business.categories.all():
            if b_c.price_month:s_monthly_price=s_monthly_price+b_c.price_month
            else:
                if b_c.parent_cat.price_month:s_monthly_price=s_monthly_price+b_c.parent_cat.price_month
            
            if b_c.price_year:s_yearly_price=s_yearly_price+b_c.price_year
            else:
                if b_c.parent_cat.price_year:s_yearly_price=s_yearly_price+b_c.parent_cat.price_year
        currency=PaymentConfigure.get_payment_settings().currency_symbol
        data['t_month']= str(currency) +str(s_monthly_price)
        data['t_year']=str(currency) +str(s_yearly_price)
    except:
        data={}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


@login_required
def user_biz_get_part_html(request):
    data = {'html': ''}
    if request.POST.get('type') == 'product':
        data['html'] = render_to_string("business/user/usr_prvw_ajax_load_product.html", {
                           'pro': BusinessProducts.objects.get(id=request.POST['id']),
                       }, context_instance=RequestContext(request))
    elif request.POST.get('type') == 'coupon':
        data['html'] = render_to_string("business/user/usr_prvw_ajax_load_coupon.html", {
                           'ofr': BusinessCoupons.objects.get(id=request.POST['id']),
                       }, context_instance=RequestContext(request))
        
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')