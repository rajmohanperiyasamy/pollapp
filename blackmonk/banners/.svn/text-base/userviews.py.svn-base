#Python
import datetime, time, calendar
from time import strptime
from datetime import timedelta, date
from dateutil import rrule, relativedelta, parser

#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q, Count
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Library
from common.utils import ds_pagination
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.staff_messages import BANNER_MSG

from banners.models import BannerZones, BannerAdvertisements, BannerSections, BannerReports, BannerPayment
from banners.forms import AddBannerForm
from payments.models import PaymentOrder
from payments.utils import get_invoice_num
from common import signals
from common.mail_utils import mail_publish_banner
from common.models import PaymentConfigure,ApprovalSettings


NO_OF_ITEMS_PER_PAGE = 10

@login_required
def manage_banners(request, template='banners/user/manage-banners.html'):
    page = int(request.GET.get('page',1))
    banners = BannerAdvertisements.objects.filter(created_by=request.user).select_related('section','zones','created_by').order_by('-id')
    banners_state = BannerAdvertisements.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status')).exclude(status='D')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
    for st in banners_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(banners,page,'banners',NO_OF_ITEMS_PER_PAGE)
    data['banner_sections'] = BannerSections.objects.filter(status = 'A').order_by('name')
    
    data['status'] = 'all'
    data['listing_type'] = 'all'
    data['created']= 'all'
    data['sort'] = '-id'
    data['total'] = total
    data['published'] = STATE['P']
    data['pending'] = STATE['N']
    data['rejected'] = STATE['R']
    data['blocked'] = STATE['B']
    return render_to_response (template, data, context_instance=RequestContext(request))

@login_required
def ajax_banner_state(request,template='banners/staff/ajax_sidebar.html'):
    ''' ajax method for retrieving banner state'''
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    
    if status == 'all':business_state = BannerAdvertisements.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status')).exclude(status='D')
    else:business_state = BannerAdvertisements.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status')).exclude(status='D')
    for st in business_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']

    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'rejected':STATE['R'],
          'blocked':STATE['B']
    }
    return HttpResponse(simplejson.dumps(data))

@login_required
def ajax_list_banners(request,template='banners/user/ajax_object_listing.html'):
    data=filter_banners(request)
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
def ajax_banner_actions(request,template='banners/user/ajax_object_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    banner = BannerAdvertisements.objects.filter(id__in=id)
    status=0

    if action=='DEL':
        for bann in banner:
            bann.delete()
        status=1
        msg=str(BANNER_MSG['BADDS'])
        mtype=get_msg_class_name('s')
    else:
        banner.update(status=action)
        '''if action=='P':
               try:
                   for buz in business:mail_publish_business(buz)
               except:pass'''
        status=1
        msg=str(BANNER_MSG['BADSUS'])
        mtype=get_msg_class_name('s')
            
    data=filter_banners(request)
    new_id=[]

    for cs in data['banners']:new_id.append(int(cs.id))
    try:
        for ai in id:all_ids.remove(ai)
    except:pass

    try:
        for ri in all_ids:
            for ni in new_id:
                if int(ni)==int(ri):
                    new_id.remove(int(ri))
    except:pass
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
    if data['total']:send_data['total']=data['total']
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['status']=status
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))

def filter_banners(request):
    ''' global method for banner sorting, earching etc...'''
    key={}
    args = q=()
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-id')
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))
    if status!='all' and status!='':key['status'] = status
    #if listing_type!='all':key['featured_sponsored'] = listing_type
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:args = (~Q(created_by = request.user))
    else:
        key['created_by'] = request.user
        

    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_section = request.GET.get('cat',None)
        if search_section:
            section = BannerSections.objects.get(id=search_section)
            key['section'] = section
        if search_type:
            if search_type=='title':key['caption__icontains'] = search_keyword
            elif search_type=='description':key['description__icontains'] = search_keyword
        if search_keyword:
            q =(Q(caption__icontains=search_keyword)|Q(section__name__icontains=search_keyword))
            if len(args) == 0 :
                banners = BannerAdvertisements.objects.filter(~Q(status='D'),q,**key).select_related('section','zones','created_by').order_by(sort)
            else:banners = BannerAdvertisements.objects.filter(~Q(status='D'),q,**key).select_related('section','zones','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :
                banners = BannerAdvertisements.objects.filter(~Q(status='D'),**key).select_related('section','zones','created_by').order_by(sort)
            else:banners = BannerAdvertisements.objects.filter(~Q(status='D'),**key).select_related('section','zones','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :banners = BannerAdvertisements.objects.filter(~Q(status='D'),**key).select_related('section','zones','created_by').order_by(sort)
        else:banners = BannerAdvertisements.objects.filter(~Q(status='D'),args,**key).select_related('section','zones','created_by').order_by(sort)
    banners = banners.distinct()
    data = ds_pagination(banners,page,'banners',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['total'] = BannerAdvertisements.objects.filter(created_by=request.user).count()
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data

@login_required
def ajax_change_banner_status(request):
    ''' ajax method for changing the banner status'''
    try:
        banner_obj = BannerAdvertisements.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        banner_obj.status = status
        '''if status=='P':
            try:mail_publish_business(business)
            except:pass'''
        banner_obj.save()
        html ='<span title="'+banner_obj.get_status().title()+'" name="'+banner_obj.status+'" id="id_estatus_'+str(banner_obj.id)+'" class="inline-block status-idty icon-'+banner_obj.get_status()+'"></span> '
        return HttpResponse(html)
    except:return HttpResponse('0')

########################################################Banner Add/Update##############################################################################

def _get_category_model(module):
    from community.models import Topic
    from bookmarks.models import BookmarkCategory
    from buzz.models import Category as BuzzCategory
    from business.models import BusinessCategory
    from article.models import ArticleCategory
    from events.models import EventCategory
    from videos.models import VideoCategory
    from gallery.models import PhotoCategory
    from attraction.models import AttractionCategory
    from deal.models import DealCategory
    #from forum.models import Category as ForumCategory
    from classifieds.models import ClassifiedCategory
    
    CATEGORY_MODELS = {'Advice':Topic, 'Bookmarks':BookmarkCategory, 'Buzz':BuzzCategory, 'Business':BusinessCategory, 
                       'Articles':ArticleCategory, 'Deals':DealCategory, 'Events':EventCategory, 
                       'Luxury-Honeymoon':AttractionCategory, 'Photos':PhotoCategory, 'Videos':VideoCategory, 'Classifieds':ClassifiedCategory }
    try:cat_model = CATEGORY_MODELS[module]
    except:cat_model = False
    return cat_model 

@login_required
def add_banner(request, template='banners/user/add-banner.html'):
    data = {}
    try:
        banner_obj = BannerAdvertisements.objects.get(id = request.REQUEST['bid'])
        old_amount = banner_obj.total_amount
        
        vv = ContentType.objects.get_for_model(banner_obj)
        pod=PaymentOrder.objects.filter(content_type=vv,object_id = banner_obj.id).reverse()
            
        tot = 0
        for po in pod:
            tot = tot+po.amount
        
        form = AddBannerForm(instance = banner_obj, sectionobj = banner_obj.section)
        msg = 'BADUS'
        data['already_paid'] = float(tot)
    except:
        import sys
        print sys.exc_info()
        banner_obj = False  
        form = AddBannerForm(sectionobj = None)
        msg = 'BADAS'
    if request.POST:
        data['selected_category'] = request.POST.get('category',False)
        data['selected_zone'] = request.POST.get('zones',False)
        data['total_impression'] = total_impression = int(request.POST.get('total_impression',0))
        data['total_amount'] = total_amount = float(request.POST.get('total_amount',0))
        if banner_obj:form = AddBannerForm(request.POST, request.FILES, instance = banner_obj, sectionobj = None)
        else:form = AddBannerForm(request.POST,request.FILES,sectionobj = None)
        if form.is_valid():
            add_banner = form.save(commit=False)
            add_banner.created_by = add_banner.modified_by = request.user
            
            ''' fk payment settings''' 
            try:
                payment_obj = BannerPayment.objects.get(id=request.POST['payment'])
                add_banner.payment = payment_obj
                if total_impression == 0:add_banner.temp_impressions = payment_obj.impressions
                else:add_banner.temp_impressions = total_impression
                if total_amount == 0:add_banner.temp_amount = int(payment_obj.price_impressions)
                else:add_banner.temp_amount = total_amount
            except:
                pass    
            if not banner_obj:
                add_banner.impressions=payment_obj.impressions
                add_banner.total_amount=payment_obj.price_impressions
                
            add_banner.payment_type = 'I'
            
            try:
                category = _get_category_model(str(add_banner.section)).objects.get(id=request.POST['category'])
                add_banner.content_object = category
            except:pass
            
            if add_banner.is_script:add_banner.image = ''
            bids=add_banner.id
            add_banner.save()
            
            appreoval_settings = ApprovalSettings.objects.get(name='banners')
            payment_mode=request.POST.get('payment_mode','offline')
            payment_settings = PaymentConfigure.get_payment_settings()
            add_banner.save()
            if payment_settings.online_payment and payment_mode=='online' and not banner_obj:
                return HttpResponseRedirect(reverse('banners_payments_confirm',args=[add_banner.id,add_banner.payment_id]))
            elif banner_obj:
                if float(add_banner.temp_amount)>float(tot):
                    if payment_mode == 'online':
                        return HttpResponseRedirect(reverse('banners_payments_confirm',args=[add_banner.id,add_banner.payment_id]))
                    else:
                        return HttpResponseRedirect(reverse('banner_payments_offline_confirm',args=[add_banner.id,add_banner.payment_id])+'?type=banners')
                else:
                    if appreoval_settings.paid_update and banner_obj.status == 'P':
                        add_banner.status = 'P'
                        mail_publish_banner(add_banner)
                    else:
                        add_banner.status = 'N'
                    add_banner.save()
                    #save_to_paymentorder(request,add_banner,add_banner.payment_type,add_banner.total_amount)
                    messages.success(request, str(BANNER_MSG[msg]))
                    #########Email Notification##########
                    signals.create_staffmail.send(sender=None,object=add_banner,module='banners',action='U',user=request.user)
                    signals.create_notification.send(sender=None,user=request.user, obj=banner_obj, not_type='updated in',obj_title=banner_obj.caption)
                    #####################################
                    return HttpResponseRedirect(reverse('user_banners_manage_banners'))
            else:
                #save_to_paymentorder(request,add_banner,add_banner.payment_type,add_banner.total_amount)
                #########Email Notification##########
                signals.create_staffmail.send(sender=None,object=add_banner,module='banners',action='A',user=request.user)
                signals.create_notification.send(sender=None,user=request.user, obj=add_banner, not_type='submitted in',obj_title=add_banner.caption)
                #####################################
                return HttpResponseRedirect(reverse('banner_payments_offline_confirm',args=[add_banner.id,add_banner.payment_id])+'?type=banners')
        else:
            print form.errors
            form = form
    data['form'] = form
    data['banner_obj'] = banner_obj 
    data['banner_zones'] = BannerZones.objects.all().order_by('name')
    if banner_obj:
        data['banner_zones_obj'] = BannerZones.objects.get(id=banner_obj.zones_id)
    return render_to_response (template, data, context_instance=RequestContext(request))

@login_required          
def ajax_delete_banner_image(request):
    ''' deleting uploaded banner image '''
    try:
        banner_obj = BannerAdvertisements.objects.get(id=request.GET['bid'])
        banner_obj.image.delete()
        banner_obj.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')
    
@login_required     
def preview_banner(request, template = 'banners/user/banner-preview.html'):
    try:banner = BannerAdvertisements.objects.get(id = request.GET['bid'])
    except: return HttpResponseRedirect(reverse('user_banners_manage_banners'))
    data={'banner':banner}
    return render_to_response (template, data, context_instance=RequestContext(request))


@login_required
def ajax_load_banner_payment(request, template='banners/user/load-banner-payments.html'):
    try:
        selected_zone = BannerZones.objects.get(id = request.GET['zone'])
        status = True
    except:
        selected_zone = None  
        status = False
    try:banner_obj = BannerAdvertisements.objects.get(id = request.REQUEST['bid'])
    except:banner_obj = None  

    banner_payments = BannerPayment.objects.all().order_by('id')
    impressions = range(5000,205000,5000)  
    
    data = {'selected_zone':selected_zone,'banner_payments':banner_payments,'impressions':impressions,'banner_obj':banner_obj}
    data['total_impression'] = int(request.GET.get('total_impression',0))
    data['total_amount'] = float(request.GET.get('total_amount',0))
    send_data = {'html':render_to_string(template,data,context_instance=RequestContext(request))}
    send_data['status'] = status
    return HttpResponse(simplejson.dumps(send_data))

@login_required
def banner_traffic_reports(request, template = 'banners/user/banner-traffic-reports.html'):
    from dateutil.relativedelta import relativedelta
    data = {}
    today = datetime.datetime.now()
    start_date =  datetime.date(2013, 1, 1)
    end_date = datetime.datetime.now() #+ relativedelta( years = +1 )
    try:banner = BannerAdvertisements.objects.get(id = request.GET['bid'])
    except: return HttpResponseRedirect(reverse('staff_banners_manage_banners'))
    msg = _('Both "Destination Url" and "Traffic Report ClickThru" has no effect when you upload script banners.')
    if banner.is_script:messages.error(request, msg)
    
    try:selected_date = parser.parse(request.GET['year'])
    except:selected_date = today
    bymonth_select = {"month": """DATE_TRUNC('month', viewed_on)"""} # Postgres specific
    banner_reports = BannerReports.objects.extra(select=bymonth_select).values('month').annotate(views=Count('viewed_on')).filter(banner = banner, is_clicked = False,viewed_on__year = selected_date.year).order_by('month')
    
    data['banner'] = banner
    years = list(rrule.rrule(rrule.YEARLY,dtstart=start_date,until=end_date))
    data['years'] = list(reversed(years))
    data['selected_date'] = selected_date 
    data['banner_reports'] = banner_reports
    return render_to_response (template, data, context_instance=RequestContext(request))  

@login_required    
def save_to_paymentorder(request,object,type,price):
    po=PaymentOrder(content_object = object)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Pending'
    po.amount = price
    po.user = request.user
    po.listing_type = type
    po.object_name=object.caption
    po.save()
    return po