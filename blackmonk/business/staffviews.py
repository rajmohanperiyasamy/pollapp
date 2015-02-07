import csv
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
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
from django.contrib.contenttypes.models import ContentType

from random import sample
from business.utils import save_to_claim_business
from business.forms import BusinessForm, AddressForm, WorkingHoursForm, \
    BusinessSEOForm, ProductForm, CouponForm, EditBusinessForm
from business.models import BusinessCategory, Attributes, AttributeValues, \
    BizAttributes, Tag, BusinessCoupons, BusinessProducts, BusinessPrice, \
    BusinessClaimSettings, WorkingHours, BusinessLogo, Business, BusinessFiles, \
    BusinessClaim
from business.tasks import process_business_csv_upload, BIZ_CSV_HEADER
from business.utils import co_add_categories, co_add_tags, business_stripe_unsubscribe
from common import signals
from common.fileupload import upload_logo, upload_files, delete_files, \
    upload_pro_cup_photo, delete_pro_cup_photos, upload_photos_forgallery, \
    delete_photos
from common.getunique import getUniqueValue, getSlugData
from common.mail_utils import mail_publish_business
from common.models import Address, CSVfile, ContactEmails
from common.staff_messages import BUSINESS_MSG, COMMON
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name
from common.utils import ds_pagination, get_lat_lng, ds_cleantext
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from payments.models import PaymentOrder
from payments.utils import get_invoice_num
from payments.stripes.models import StripeUnsubscribers, StripePaymentDetails

business_album_cat = PhotoCategory.objects.get_or_create(name="Business", slug='business', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
PAY_MONTH_CHOICES = ((1, '1month'),(3, '3month'),(6, '6month'),(12, '1year'),)
NO_OF_ITEMS_PER_PAGE=10


######################################################################################################################
###########################################      BUSINESS      #######################################################
######################################################################################################################


@staff_member_required
def manage_business(request,template='business/staff/home.html'):
    business = Business.objects.all().select_related('category','created_by').order_by('-created_on')
    business_state = Business.objects.values('status').annotate(s_count=Count('status'))

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

    try:
        message=request.GET['message']
        message=message.split(',')
        data['msg']= _('Out of %(count1)s business %(count2)s business has been added successfully') % {'count1': message[0], 'count2': message[1]}
    except:pass

    data['categories'] = BusinessCategory.objects.filter(parent_cat__isnull=True).select_related('parent_cat').order_by('name')
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['drafted'] =STATE['D']
    data['search'] =False
    try:data['recent'] = request.GET['pending_business']
    except:data['recent'] = False
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def ajax_business_state(request,template='business/staff/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    if status == 'all':
        business_state = Business.objects.values('status').annotate(s_count=Count('status'))
    else:
        business_state = Business.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in business_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']

    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'rejected':STATE['R'],
          'drafted':STATE['D'],
          'blocked':STATE['B']
    }
    return HttpResponse(simplejson.dumps(data))


@staff_member_required
def ajax_list_business(request,template='business/staff/ajax_listing.html'):
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


@staff_member_required
def ajax_business_action(request,template='business/staff/ajax_delete_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    businesslist = Business.objects.filter(id__in=id)
    status=0
    if action=='DEL':
        if request.user.has_perm('business.delete_business'):
            signals.celery_delete_indexs.send(sender=None,objects=businesslist)
            for business in businesslist:
                try:
                    business_stripe_unsubscribe(business.id)
                    business.album.delete()
                except:
                    pass
            businesslist.delete()
            status=1
            msg=str(BUSINESS_MSG['BDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('business.publish_business'):
            businesslist.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=businesslist)
            if action=='P':
                try:
                    for business in businesslist:mail_publish_business(business)
                except:pass
            status=1
            msg=str(BUSINESS_MSG['BSCS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    
    for business in businesslist:
        business.save()
        for log in business.audit_log.all()[:1]:
            log.action_type = action
            log.save()
    data=filter(request)
    new_id=[]

    for cs in data['business']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
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
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['status']=status
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))


def filter(request):
    data={}
    key={}
    args = q=()
    msg = False
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
    if listing_type!='all':key['featured_sponsored'] = listing_type
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:args = (~Q(created_by = request.user))

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
            else:key['created_by__display_name__icontains'] = search_keyword

        if search_keyword:
            q =(Q(name__icontains=search_keyword)|Q(categories__name__icontains=search_keyword)|Q(summary__icontains=search_keyword)|Q(description__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if len(args) == 0 :
                business = Business.objects.filter(q,**key).select_related('categories','created_by').order_by(sort)
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
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    if search:
        data['catgy']=search_category
    data['item_perpage']=item_perpage
    return data

@staff_member_required
def ajax_list_business_claim(request,template='business/staff/ajax_listing.html'):
    biz_ids = []
    option=request.GET['claim']
    if option=='all':
        biz_ids = BusinessClaim.objects.all().values_list('business__id', flat=True)
    elif option=='0':
        biz_ids = BusinessClaim.objects.filter(is_approved=False).values_list('business__id', flat=True)
    elif option=='1':
        biz_ids = BusinessClaim.objects.filter(is_approved=True).values_list('business__id', flat=True)
    elif option=='3':
        biz_ids = StripePaymentDetails.objects.filter(subscription_status='onhold').values_list('object_id', flat=True)
    business = Business.objects.filter(id__in=biz_ids).select_related('categories','created_by').order_by('-id')
    business=business.distinct()
    data ={'business':business}
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    send_data={'count':business.count()}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps(send_data))


@staff_member_required
@permission_required('business.publish_business',raise_exception=True)
def ajax_list_business_claim_status(request,template='business/staff/ajax_claim_status.html'):
    data={}
    data['business'] = business = Business.objects.get(id=int(request.REQUEST['id']))
    data['claim'] = claim = BusinessClaim.objects.get(business=business)
    if request.method=='POST':
        option=request.POST['option']
        if option in ['RP','RN','RB']:
            claim.delete()
            business.is_claimable = True
        else:
            save_to_claim_business(business=business, approve=True, paid=True)
        business.status = option[-1]
        business.save()
        signals.celery_update_index.send(sender=None,object=business)
        return HttpResponse(simplejson.dumps({'status':1,'id':business.id,'mtype':get_msg_class_name('s'),'msg':str(BUSINESS_MSG['BUS'])}))
    return render_to_response(template,data,context_instance = RequestContext(request))

@staff_member_required
@permission_required('business.publish_business',raise_exception=True)
def change_status_business(request):
    try:
        business = Business.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        business.status = status
        if status=='P':
            try:mail_publish_business(business)
            except:pass
        business.save()
        for log in business.audit_log.all()[:1]:
            log.action_type = status
            log.save()
        signals.celery_update_index.send(sender=None,object=business)
        html ='<span title="'+business.get_status().title()+'" name="'+business.status+'" id="id_estatus_'+str(business.id)+'" class="inline-block status-idty icon-'+business.get_status()+'"></span> '
        return HttpResponse(html)
    except:return HttpResponse('0')

@staff_member_required
@permission_required('business.change_business',raise_exception=True)
def seo_business(request,id,template='business/staff/update_seo.html'):
    business = Business.objects.get(id = id)
    form=BusinessSEOForm(instance=business)
    if request.POST:
        form=BusinessSEOForm(request.POST,instance=business)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug=getUniqueValue(Business,slugify(business.slug),instance_pk=seo.id)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(BUSINESS_MSG['BSUS'])}))
        else:
            data={'form':form,'business':business}
            return error_response(request,data,template,BUSINESS_MSG)
    data={'form':form,'business':business}
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('business.promote_business',raise_exception=True)
def business_listing_type(request,template='business/staff/ajax_listing_type.html'):
    data={}
    data['business'] =business= Business.objects.get(id=int(request.REQUEST['id']))
    buz_obj =Business.objects.get(id=int(request.REQUEST['id']))
    payment_type = buz_obj.payment_type
    if payment_type == 'M':
        payment_type = 'Monthly'
    else:
        payment_type = 'Yearly'
    data['payment_type'] =payment_type
    if request.method=='POST':
        listing_type=BusinessPrice.objects.get(id=int(request.POST['listingtype']))
        if listing_type.level=='level2':business.featured_sponsored='F'
        elif listing_type.level=='level1':business.featured_sponsored='S'
        else:business.featured_sponsored='B'
        business.is_paid = request.POST['is_paid'] == "on"
        try:
            if request.POST['period']:business.payment_type=request.POST['period']
        except:pass
        try:
            dfmt = '%d/%m/%Y'
            business.lstart_date=datetime.datetime.strptime(request.POST['start_date'], dfmt)
            business.lend_date=datetime.datetime.strptime(request.POST['end_date'], dfmt)
        except:
            business.lstart_date = datetime.datetime.now()
            business.lend_date =   datetime.datetime.now()
        business.payment=listing_type
        business.save()
        
        loglist = business.audit_log.all()[:1]
        for log in loglist:
            log.delete()
            
        signals.celery_update_index.send(sender=None,object=business)
        business.sp_cost = request.POST['price_'+str(listing_type.id)]
        if listing_type.level!='level0':
            save_to_paymentorder(request,business,listing_type.level_label, business.lstart_date, business.lend_date)
        business.save()
        
        loglist = business.audit_log.all()[:1]
        for log in loglist:
            if business.featured_sponsored == 'B':log.action_type = 'N'
            else:log.action_type = business.featured_sponsored
            log.save()
        
        return HttpResponse(simplejson.dumps({'status':1,'listingtype':business.featured_sponsored,'id':business.id,'mtype':get_msg_class_name('s'),'msg':str(BUSINESS_MSG['BLUS'])}))
            ####################################PAYMENT####################################
    data['business_price_objects']=BusinessPrice.objects.all().order_by('id')
    bus_cat=[]
    for bcat in business.categories.all() :
        bus_cat.append(bcat.id)
    category=BusinessCategory.objects.filter(id__in=bus_cat).exclude(parent_cat__isnull=True)
    mpay=ypay=0
    for cat in category:
        if cat.price_month:mpay+=cat.price_month
        else:
            if cat.parent_cat.price_month:mpay+=cat.parent_cat.price_month
        if cat.price_year:ypay+=cat.price_year
        else:
            if cat.parent_cat.price_year:ypay+=cat.parent_cat.price_year
    data['ypay']=ypay
    data['mpay']=mpay
    return render_to_response(template,data,context_instance = RequestContext(request))


##@transaction.commit_on_success
@staff_member_required
@permission_required('business.add_business',raise_exception=True)
def add_business(request):
    category = BusinessCategory.objects.filter(parent_cat=None).order_by('name')
    date = datetime.datetime.now()
    formdata = {'lstart_date':date,'lend_date':datetime.date.today()+relativedelta( months = +1 )}
    form = BusinessForm(initial=formdata)
    wform = WorkingHoursForm()
    aform = AddressForm()
    if request.POST:
        form = BusinessForm(request.POST)
        wform=WorkingHoursForm(request.POST)
        aform=AddressForm(request.POST)
        if form.is_valid() and wform.is_valid() and aform.is_valid():
            business = form.save(commit=False)
            business.created_by=business.modified_by=request.user
            save_type = request.POST['save_button']
            if save_type == 'publish':
                business.status='P'
            else:
                business.status='N'
            business.operating_hours=int(request.POST['operating_hours'])
            try:business.logo=BusinessLogo.objects.get(id=int(request.POST['new_pic']))
            except:pass
            business.slug = getUniqueValue(Business,slugify(getSlugData(request.POST['slug'])))
            business.created_by = business.modified_by = request.user
            
            if business.operating_hours:
                workinghour=wform.save(commit=False)
                workinghour.status='P'
                workinghour.save()
                business.workinghours=workinghour
            
            business.save()

            seo_category = ''
            for category in business.categories.all():seo_category = seo_category+category.name.strip()+','
            business.seo_title = business.name.strip()
            business.seo_description = ds_cleantext(strip_tags(business.description[:250]).strip())

            form.save_m2m()

            from common.utils import get_global_settings
            global_settings = get_global_settings()

            address=aform.save(commit=False)
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
                    if request.POST['attr_'+str(attr.id)].strip()!='':
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
            
            try:
                listing_type=BusinessPrice.objects.get(id=int(request.POST['listingtype']))
                if listing_type.level=='level2':business.featured_sponsored='F'
                elif listing_type.level=='level1':business.featured_sponsored='S'
                else:business.featured_sponsored='B'
    
                if listing_type.level!='level0':
                    business.sp_cost=request.POST['price_'+str(listing_type.id)]
                    business.is_paid=True
                    business.payment_type=request.POST['period']
                    save_to_paymentorder(request,business,listing_type.level_label, business.lstart_date, business.lend_date)
                else:business.is_paid=False
                business.payment=listing_type
            except:
                business.featured_sponsored='B'
                business.is_paid=False
            #business.payment=listing_type
            business.save()
            
            for log in business.audit_log.all():
                if log.action_type=='U':
                    log.delete()

            co_add_tags(business,request.POST['tags'])
            co_add_categories(business, request.POST.getlist('sub_category'))
            signals.celery_update_index.send(sender=None,object=business)
            files=BusinessFiles.objects.filter(id__in=request.POST.getlist('new_files'))
            files.update(business=business)
            messages.success(request, str(BUSINESS_MSG['BAS']))
            return HttpResponseRedirect(reverse('staff_preview_business',args=[business.id]))

    data = { 'category': category, 'form':form}
    data['wform']=wform
    data['aform']=aform
    data['claim']=BusinessClaimSettings.get_setting()
    data['business_price_objects']= BusinessPrice.objects.filter(level_visibility=True).order_by('id')
    return render_to_response('business/staff/add_business.html', data, context_instance=RequestContext(request))



@staff_member_required
@permission_required('business.change_business',raise_exception=True)
def update_business(request,id):
    business=Business.objects.get(id=id)
    try:whour=WorkingHours.objects.get(id=business.workinghours.id)
    except:whour=None
    address=business.primary_address()
    try:albumid = business.album_id
    except:albumid = None

    form= EditBusinessForm(instance=business)
    wform=WorkingHoursForm(instance=whour)
    aform=AddressForm(instance=address)
    if request.method=='POST':
        form = EditBusinessForm(request.POST,instance=business)
        wform=WorkingHoursForm(request.POST,instance=whour)
        aform=AddressForm(request.POST,instance=address)
        if form.is_valid() and wform.is_valid() and aform.is_valid():
            business = form.save(commit=False)
            business.modified_by = request.user
            business.operating_hours = int(request.POST['operating_hours'])
            try:
                business.logo = BusinessLogo.objects.get(id=int(request.POST['new_pic']))
            except:
                pass
            business.slug = getUniqueValue(Business,slugify(getSlugData(request.POST['slug'])),instance_pk=business.id)
            business.modified_by = request.user
            business.album_id = albumid
            business.save()
            form.save_m2m()
            if business.operating_hours:
                workinghour=wform.save(commit=False)
                workinghour.status='P'
                workinghour.save()
                business.workinghours=workinghour
                business.save()
                loglist = business.audit_log.all()[:1]
                for log in loglist:
                    log.delete()

            from common.utils import get_global_settings
            global_settings = get_global_settings()

            address = aform.save(commit=False)
            address.status='P'
            address.created_by = address.modified_by = request.user
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            address.save()
            if business.address:business.address.clear()
            business.address.add(address)

            cat=request.POST.getlist('sub_category')
            cat.append(request.POST['category'])
            attribute=Attributes.objects.filter(category_id__in=cat).order_by('attribute_group').distinct()


            claer_atr=BizAttributes.objects.filter(business=business)
            claer_atr.delete()
            try:
                for attr in attribute:
                    if attr.type == 'C':
                        if request.POST['attr_'+str(attr.id)].strip()!='':
                            try:
                                atr=BizAttributes.objects.get(business=business,key=attr)
                                atr.textbox_value=request.POST['attr_'+str(attr.id)]
                                atr.save()
                            except:
                                atr=BizAttributes(business=business,key=attr)
                                atr.textbox_value=request.POST['attr_'+str(attr.id)]
                                atr.save()
                    else:
                        try:atr=BizAttributes.objects.get(business=business,key=attr)
                        except:atr=BizAttributes(business=business,key=attr)
                        for av in request.POST.getlist('attr_'+str(attr.id)):
                            atr.save()
                            atr.value.add(AttributeValues.objects.get(id=av))
            except:pass                

            co_add_tags(business,request.POST['tags'])
            co_add_categories(business, request.POST.getlist('sub_category'))
            messages.success(request, str(BUSINESS_MSG['BUS']))
            signals.celery_update_index.send(sender=None,object=business)
            return HttpResponseRedirect(reverse('staff_manage_business'))

    category = BusinessCategory.objects.filter(parent_cat=None).order_by('name')
    data = { 'category': category, 'form':form,'business':business,'address':address}
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
    data['claim']=BusinessClaimSettings.get_setting()
    return render_to_response('business/staff/update_business.html', data, context_instance=RequestContext(request))


def ajax_upload_photos(request):
    if request.method == "POST":
        business = Business.objects.get(id=request.GET['id'])
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
        try:
            alllog = business.audit_log.all()
            log1 = alllog[0]
            log1.action_type = 'G'
            log1.save()
            log2 = alllog[1]
            
            if log1.action_type == log2.action_type and log1.modified_by == log2.modified_by:
                log1.delete()
        except:
            pass
        response = upload_photos_forgallery(request,Photos,album,'album')
        album.save()
        return response
    else:
        business = Business.objects.get(id=request.GET['id'])
        album = business.album
        return upload_photos_forgallery(request,Photos,album,'album')
 
def ajax_upload_cover_photos(request):
    if request.method == "POST":
        try:
            business = Business.objects.get(id=request.GET['id'])
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
            response = upload_photos_forgallery(request,Photos,album,'album',featured=True)
            album.save()
            return response
        except:
            from sys import exc_info
            return HttpResponse(str(exc_info()))
            pass

"""
##################################################################################################################
#######################################    PREVIEW PRODUCT COUPON IMAGE     ######################################
##################################################################################################################
"""
@staff_member_required
def preview_business(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id)
    try:data['msg'] =BUSINESS_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    return render_to_response('business/staff/preview.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_images(request,id):
    if not request.user.has_perm('business.add_business') and not request.user.has_perm('business.change_business'):
        raise PermissionDenied
    data={}
    data['business']=business= Business.objects.get(id=id)
    return render_to_response('business/staff/images.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_product(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id)
    data['products']=BusinessProducts.objects.filter(business=business).order_by('-created_on')
    return render_to_response('business/staff/product.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_update_product(request,bid,id=None):
    if not request.user.has_perm('business.add_business') and not request.user.has_perm('business.change_business'):
        raise PermissionDenied
    data={}
    data['business']=business= Business.objects.get(id=bid)
    if id:
        data['product']=product=BusinessProducts.objects.get(id=id)
        form=ProductForm(instance=product)
    else:form=ProductForm()
    if request.method=='POST':
        if id:form=ProductForm(request.POST,instance=product)
        else:form=ProductForm(request.POST)
        if form.is_valid():
            product=form.save(commit=False)
            product.business=business
            product.description=product.description[:1000]
            product.is_active=True
            product.created_by=request.user
            product.save()
            if id:
                return HttpResponse(simplejson.dumps({'status':1,'id':product.id,'msg':str(BUSINESS_MSG['BPUS']),'mtype':get_msg_class_name('s')}))
            else:
                return HttpResponse(simplejson.dumps({'status':1,'id':product.id,'msg':str(BUSINESS_MSG['BPAS']),'mtype':get_msg_class_name('s')}))
        else:
            data['form']=form
            html=render_to_string('business/staff/update_product.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    data['form']=form
    return render_to_response('business/staff/update_product.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_delete_product(request):
    try:
        if request.user.has_perm('business.add_business') and request.user.has_perm('business.change_business'):
            product=BusinessProducts.objects.get(id=int(request.POST['id']))
            product.delete()
            return HttpResponse(simplejson.dumps({'status':1,'msg':str(BUSINESS_MSG['BPDS']),'mtype':get_msg_class_name('s')}))
        else:
            return HttpResponse(simplejson.dumps({'status':0,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    except:
        return HttpResponse(simplejson.dumps({'status':0,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

@staff_member_required
def business_product_load_html(request):
    try:
        if request.user.has_perm('business.add_business') and request.user.has_perm('business.change_business'):
            product=BusinessProducts.objects.get(id=int(request.POST['id']))
            html=render_to_string('business/staff/load_product.html',{'product':product},context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'html':html,'status':1}))
        else:return HttpResponse(simplejson.dumps({'status':0}))
    except:return HttpResponse(simplejson.dumps({'status':0}))
############################################################################################################
############################################################################################################
############################################################################################################
@staff_member_required
def business_coupon(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id)
    data['coupons']=BusinessCoupons.objects.filter(business=business)
    return render_to_response('business/staff/coupon.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_update_coupon(request,bid,id=None):
    if not request.user.has_perm('business.add_business') and not request.user.has_perm('business.change_business'):
        raise PermissionDenied
    data={}
    data['business']=business= Business.objects.get(id=bid)
    if id:
        data['coupon']=coupon=BusinessCoupons.objects.get(id=id)
        form=CouponForm(instance=coupon)
    else:form=CouponForm()
    if request.method=='POST':
        if id:form=CouponForm(request.POST,instance=coupon)
        else:form=CouponForm(request.POST)
        if form.is_valid():
            coupon=form.save(commit=False)
            coupon.business=business
            coupon.is_active=True
            coupon.created_by=request.user
            coupon.save()
            if id:
                return HttpResponse(simplejson.dumps({'status':1,'id':coupon.id,'msg':str(BUSINESS_MSG['BCUS']),'mtype':get_msg_class_name('s')}))
            else:
                return HttpResponse(simplejson.dumps({'status':1,'id':coupon.id,'msg':str(BUSINESS_MSG['BCAS']),'mtype':get_msg_class_name('s')}))
        else:
            data['form']=form
            html=render_to_string('business/staff/update_coupon.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    data['form']=form
    return render_to_response('business/staff/update_coupon.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_delete_coupon(request):
    try:
        if request.user.has_perm('business.add_business') and  request.user.has_perm('business.change_business'):
            product=BusinessCoupons.objects.get(id=int(request.POST['id']))
            product.delete()
            return HttpResponse(simplejson.dumps({'status':1,'msg':str(BUSINESS_MSG['BCDS']),'mtype':get_msg_class_name('s')}))
        else:return HttpResponse(simplejson.dumps({'status':0,'msg':str(COMMON['DENIED']),'mtype':get_msg_class_name('w')}))
    except:return HttpResponse(simplejson.dumps({'status':0,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

@staff_member_required
def business_coupon_load_html(request):
    try:
        if request.user.has_perm('business.add_business') and request.user.has_perm('business.change_business'):
            coupon=BusinessCoupons.objects.get(id=int(request.POST['id']))
            html=render_to_string('business/staff/load_coupon.html',{'coupon':coupon},context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'html':html,'status':1}))
        else:return HttpResponse(simplejson.dumps({'status':0}))
    except:
        return HttpResponse(simplejson.dumps({'status':0}))
############################################################################################################
############################################################################################################
############################################################################################################
@staff_member_required
def business_address(request,id):
    data={}
    data['business']=business= Business.objects.get(id=id)
    data['buz_address']=Address.objects.filter(business=business)
    return render_to_response('business/staff/address.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_update_address(request,bid,id=None):
    data={}
    data['business']=business= Business.objects.get(id=bid)
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
            html=render_to_string('business/staff/update_address.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    data['form']=form
    return render_to_response('business/staff/update_address.html',data,context_instance=RequestContext(request))

@staff_member_required
def business_delete_address(request):
    try:
        address=Address.objects.get(id=int(request.POST['id']))
        address.delete()
        return HttpResponse(simplejson.dumps({'status':1,'msg':str(BUSINESS_MSG['BADS']),'mtype':get_msg_class_name('s')}))
    except:return HttpResponse(simplejson.dumps({'status':0,'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

"""
##################################### Manage Enquires #############################################
"""
@staff_member_required
def manage_enquiry(request,id,template='common/manage_enquiry.html'):
    page = int(request.GET.get('page',1))
    business = Business.objects.get(id = id)
    vv = ContentType.objects.get_for_model(business)
    contacts_list = ContactEmails.objects.filter(content_type=vv,object_id = business.id)
    data = ds_pagination(contacts_list,page,'contacts_list',NO_OF_ITEMS_PER_PAGE)
    data['sort'] = "-created_on"
    data['module'] = 'business'
    return render_to_response(template,data,context_instance = RequestContext(request))

"""
##################################################################################################################
#######################################          COMMON FUNCTIONS           ######################################
##################################################################################################################
"""

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
    html=render_to_string('business/update_attribute.html', data, context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'html':html,'mpay':mpay,'ypay':ypay}))

@staff_member_required
def auto_suggest_tag(request):
    try:
        data = Tag.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:
        data = Tag.objects.all()[:10]
    child_dict = []
    for tag in data :
        buf={'label':tag.tag,'id':tag.id,'value':tag.tag}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), mimetype='application/javascript')


@login_required
def ajax_upload_product_photo(request):
    id=int(request.REQUEST['pr_id'])
    try:
        business = Business.objects.get(id=int(request.GET['id']))
    except:business=None
    return upload_pro_cup_photo(request,BusinessProducts,business,id)

@login_required
def business_delete_product_photo(request,pk):
    return delete_pro_cup_photos(request,BusinessProducts,pk)

@login_required
def ajax_upload_coupon_photo(request):
    id=int(request.REQUEST['pr_id'])
    try:business = Business.objects.get(id=int(request.GET['id']))
    except:business=None
    return upload_pro_cup_photo(request,BusinessCoupons,business,id)

@login_required
def business_delete_coupon_photo(request,pk):
    return delete_pro_cup_photos(request,BusinessCoupons,pk)


@login_required
def ajax_upload_logo(request):
    try:business = Business.objects.get(id=int(request.GET['id']))
    except:business=None
    return upload_logo(request,BusinessLogo,business)

@login_required
def business_delete_logo(request,pk):
    return delete_photos(request,BusinessLogo,pk)

@login_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,BusinessPhoto,pk)

@login_required
def ajax_upload_files(request):
    try:business = Business.objects.get(id=int(request.GET['id']))
    except:business=None
    return upload_files(request,BusinessFiles,business,'business')

@login_required
def business_delete_files(request,pk):
    return delete_files(request,BusinessFiles,pk)

@staff_member_required
def save_to_paymentorder(request,business,business_type,start_date,end_date):
    po=PaymentOrder(content_object = business)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Success'
    po.amount = business.sp_cost
    po.user = request.user
    po.listing_type = str(business_type)+' Business'
    po.start_date=start_date
    po.end_date=end_date
    po.object_name=business.get_payment_title()
    po.save()
    return True

# Variables used for CSV
LISTING_TYPE_VAL = {'F':'FEATURED','S':'SPONSORED','B':'FREE'}
BIZ_STATUS_VAL = {'P':'PUBLISHED','N':'PENDING','R':'REJECTED','B':'BLOCKED','D':'DRAFTED'}
MAX_UPLOAD_FILESIZE = 2097152

@staff_member_required
@permission_required('business.add_business',raise_exception=True)
def business_import_csv(request):
    if request.method=='POST':
        inputfile = request.FILES['businesscsv']
        if inputfile.size > MAX_UPLOAD_FILESIZE:
            messages.error(request, "The file is too big, please make sure the size of your file is less than or equals 2Mb!")
            return HttpResponseRedirect(reverse('staff_business_import_csv'))
        else:
            csvfile = CSVfile(
                file=inputfile,
                module='business',
                status='N',
                uploaded_by=request.user
            )
            csvfile.save()
            process_business_csv_upload.delay(csvfile)
            older_files = CSVfile.objects.filter(module='business').order_by('-uploaded_on').values_list('id', flat=True)[5:]
            CSVfile.objects.filter(id__in=older_files).delete()
            messages.success(request, "Your business listings are being added,\nyou will receive notification through email once completed!")
            return HttpResponseRedirect(reverse('staff_manage_business'))
    else:
        data = {
            'filehistory': CSVfile.objects.filter(module='business').order_by('-uploaded_on'),
        }
        return render_to_response('business/staff/import_csv.html', data, context_instance=RequestContext(request))
    

@staff_member_required
def business_export_csv(request,template='business/staff/export_csv.html'):
    data = {}
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    if request.method == "POST":
        try:data['start_date'] = start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y")
        except:data['start_date'] = start_date = False
        try:data['end_date'] = end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y")
        except:data['end_date'] = end_date = False
        data['order'] = order = request.POST.get('order','-id')
        data['ltype'] = ltype = request.POST.getlist('ltype',None)
        data['status'] = status = request.POST.getlist('status',None)
        data['category'] = category = request.POST.getlist('category',None)
        key={}
        if start_date and end_date:
            key['created_on__range']=[start_date,end_date]
            sdate=request.POST['start_date'].replace('/','-')
            edate=request.POST['end_date'].replace('/','-')
            file_name='business_'+sdate+'_to_'+edate
        else:
            file_name='business'
        
        if ltype:
            key['featured_sponsored__in'] = ltype
        if status:
            key['status__in'] = status
        if category:
            key['categories__parent_cat__id__in'] = category
            
        if key:
            business = Business.objects.filter(**key).order_by(order)
        else:
            business = Business.objects.all().order_by(order)

        if not business.count():
            data['categorys'] = BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('name')
            data['error_msg'] = _('No records were found for your search. Please try again!')
            return render_to_response (template, data, context_instance=RequestContext(request))

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment;filename="%s.csv"'%(file_name)
        writer = csv.writer(response)
        writer.writerow(BIZ_CSV_HEADER)
        for buz in business:
            logo = global_settings.website_url + buz.logo.logo.url if buz.logo else ''
            parent_category = buz.get_parent_cat().name
            category = ','.join(buz.categories.values_list('name', flat=True))
            status = BIZ_STATUS_VAL[buz.status]
            listing_type = LISTING_TYPE_VAL[buz.featured_sponsored] if buz.featured_sponsored else LISTING_TYPE_VAL['B']
            payment_type = {'M': 'MONTHLY', 'Y': 'YEARLY'}[buz.payment_type] if buz.payment_type else ""
            payment_options = ','.join(buz.paymentoptions.values_list('name', flat=True))
            tags = ','.join(buz.tags.values_list('tag', flat=True))
            address = buz.primary_address()
            address_list = [
                address.address1, address.address2, address.zip, address.city, address.telephone1, address.mobile,
                address.email, address.website, address.lat, address.lon, address.zoom
            ] if address else ['', '', '', '', '', '', '', '', '', '', '']
            workinghours = buz.workinghours
            timing_list = [
                'TRUE',workinghours.notes,workinghours.mon_start,workinghours.mon_end,workinghours.tue_start,
                workinghours.tue_end,workinghours.wed_start,workinghours.wed_end,workinghours.thu_start,
                workinghours.thu_end,workinghours.fri_start,workinghours.fri_end,workinghours.sat_start,
                workinghours.sat_end,workinghours.sun_start,workinghours.sun_end,
            ] if workinghours else ['FALSE','', '', '', '', '', '', '', '', '', '','','','','','']
            business_list=[
                buz.name.encode('utf-8').strip(),
                logo,
                parent_category,
                category,
                buz.description.encode('utf-8').strip(),
                buz.seo_title.encode('utf-8').strip(),
                buz.seo_description.encode('utf-8').strip(),
                status,
                listing_type,
                buz.sp_cost,
                buz.lstart_date.strftime('%m/%d/%y') if buz.lstart_date else "",
                buz.lend_date.strftime('%m/%d/%y') if buz.lend_date else "",
                payment_type,
                ['FALSE', 'TRUE'][buz.is_paid],
                buz.fb_url, buz.twitter_url, buz.gooleplus_url,
                ['FALSE', 'TRUE'][buz.is_claimable],
                payment_options,
                tags
            ]
            business_list.extend(address_list)
            business_list.extend(timing_list)
            business_list = [smart_unicode(text).encode('utf-8', 'ignore') for text in business_list]
            writer.writerow(business_list)
        return response
    else:
        data['categorys'] = BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('name')
        return render_to_response (template, data, context_instance=RequestContext(request))
    
from business.utils import business_stripe_unsubscribe
from common.mail_utils import business_unsubscribe_user_notification
@staff_member_required
def ajax_biz_unsubscription(request,template='business/staff/ajax_biz_unsubscription.html'):
    data={}
    data['business'] = business = Business.objects.get(id=int(request.REQUEST['id']))
    data['unsub'] = unsub = StripeUnsubscribers.objects.filter(stripe_details__object_id=business.id)[0]
    stripe_obj = unsub.stripe_details
    if request.method=='POST':
        option=request.POST['option']
        free_level = BusinessPrice.objects.get(level='level0')
        if option == 'R':
            stripe_obj.subscription_status='active'
        elif option == 'UP':
            business.is_paid = False
            business.featured_sponsored = "B"
            business.status = "P"
            business.payment = free_level 
            stripe_obj.subscription_status='inactive'
            business_stripe_unsubscribe(business.id)
        elif option == 'UB':
            business.is_paid = False
            business.featured_sponsored = "B"
            business.status = "D"
            business.payment = free_level
            stripe_obj.subscription_status='inactive'
            business_stripe_unsubscribe(business.id)
        stripe_obj.save()
        business.save()
        business_unsubscribe_user_notification(stripe_obj.id,unsub.email)
        unsub.delete()
        
        return HttpResponse(simplejson.dumps({'status':1,'id':business.id,'mtype':get_msg_class_name('s'),'msg':str("Unsubscription Request Succesfully Processed")}))
    return render_to_response(template,data,context_instance = RequestContext(request))

