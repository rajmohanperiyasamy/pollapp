from datetime import timedelta, date
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.html import strip_tags
from random import sample

from classifieds.forms import ClassifiedUserForm, UserClassifiedSeoForm, \
    EditClassifiedForm, AddressForm
from classifieds.models import ClassifiedReport, ClassifiedPrice, Address, \
    Classifieds, ClassifiedCategory, ClassifiedAttribute, ClassifiedAttributevalue, \
    Tag as ClassifiedTag
from classifieds.utils import save_classified_tags, save_classified_attribute, \
    save_classifieds_photos, save_classified_address
from common import signals
from common.fileupload import upload_photos_forgallery, delete_photos
from common.getunique import getUniqueValue, getSlugData
from common.mail_utils import mail_publish_classifieds
from common.models import ApprovalSettings, PaymentConfigure
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name
from common.user_messages import CLASSIFIED_MSG
from common.utils import ds_pagination, get_lat_lng, ds_cleantext, \
    get_global_settings
from common.utilviews import crop_and_save_coverphoto
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from locality.models import Locality
from payments.models import PaymentOrder
from payments.utils import get_invoice_num, save_to_offline_payment


classified_album_cat = PhotoCategory.objects.get_or_create(name="Classifieds", slug='classifieds', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'


NO_OF_ITEMS_PER_PAGE=10
status_dict = {
    'Rejected': 'R',
    'Draft': 'D',
    'Published': 'P',
    'Expired': 'E',
    'Pending': 'N',
    'Blocked': 'B',
}
"""
###################################################################################################################
############################################    CLASSIFIEDS    ####################################################
###################################################################################################################
"""

@login_required
def list_classified(request,template='classifieds/user/content_manager.html'):
    show = request.GET.get('show', None)
    if show is None:
        classified = Classifieds.objects.filter(created_by=request.user).select_related('category','created_by').order_by('-created_on')
    else:
        classified = Classifieds.objects.filter(status=status_dict[show], created_by=request.user).select_related('category','created_by').order_by('-created_on')
    classifieds_state = Classifieds.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))
    
    page = int(request.GET.get('page',1))
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
    for st in classifieds_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(classified,page,'classified',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =CLASSIFIED_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['drafted'] =STATE['D']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['expired'] =STATE['E']
    data['search'] =False
    if show is not None:
        data['show'] = status_dict[show]
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def ajax_list_classified(request,template='classifieds/user/ajax_object_listing.html'):
    data=filter_classifieds(request)
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
def ajax_classified_action(request,template='classifieds/user/ajax_object_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    action=request.GET['action']
    action_classifieds = Classifieds.objects.filter(id__in=id,created_by=request.user)
    cls_count=action_classifieds.count()
    
    if action=='DEL':
        for class_del in action_classifieds:
            signals.create_notification.send(sender=None,user=request.user, obj=class_del, not_type='deleted from',obj_title=class_del.title)
            signals.celery_delete_index.send(sender=None,object=class_del)
            try:class_del.album.delete()
            except:pass
        action_classifieds.delete()
        msg=str(CLASSIFIED_MSG['CDS'])
        mtype=get_msg_class_name('s')
    else:
        action_classifieds.update(status=action)
        signals.celery_update_indexs.send(sender=None,objects=action_classifieds)
        msg=str(CLASSIFIED_MSG['CSCS'])
        mtype=get_msg_class_name('s')
    data=filter_classifieds(request)
    
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
    send_data['total'] = Classifieds.objects.filter(created_by=request.user).count()
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['item_perpage']=data['item_perpage']   
    return HttpResponse(simplejson.dumps(send_data))

   
def filter_classifieds(request):
    data=key={}
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
    
    key['created_by'] = request.user
   
    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':key['listing_type'] = listing_type
    
    
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        
        if search_category:
            categorys = ClassifiedCategory.objects.select_related("parent").get(id=search_category)
            if categorys.parent: key['category'] = categorys
            else:
                categorys = ClassifiedCategory.objects.filter(parent=categorys)
                key['category__in'] = categorys
        
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='desc':key['description__icontains'] = search_keyword
        
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(description__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if len(args) == 0 :classified = Classifieds.objects.filter(q,**key).select_related('category','created_by').order_by(sort)
            else:classified = Classifieds.objects.filter(q,**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :classified = Classifieds.objects.filter(**key).select_related('category','created_by').order_by(sort)
            else:classified = Classifieds.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :classified = Classifieds.objects.filter(**key).select_related('category','created_by').order_by(sort)
        else:classified = Classifieds.objects.filter(args,**key).select_related('category','created_by').order_by(sort)
    
    classified=classified.distinct()
    data = ds_pagination(classified,page,'classified',item_perpage)
    data['status'] = status
    if search:
        data['search_keyword'] = request.GET.get('kwd',"").strip()
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 


@login_required
def ajax_classified_state(request,template='classifieds/user/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
    classifieds_state = Classifieds.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in classifieds_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'expired':STATE['E']
    }
    return HttpResponse(simplejson.dumps(data))


@login_required
def classified_upgrade_listing_type(request,id,template='classifieds/user/ajax_listing_type.html'):
    data={}
    try:classifieds_obj = Classifieds.objects.get(id = id,created_by=request.user)#,status='D'
    except:
        messages.error(request, str(CLASSIFIED_MSG['OOPS']))
        return HttpResponseRedirect(reverse('user_classified_home'))
    payment_settings=PaymentConfigure.get_payment_settings()
    if request.POST :
        try:
            classifieds_price_obj = ClassifiedPrice.objects.get(level = request.POST['payment_level'])
            appreoval_settings = ApprovalSettings.objects.get(name='classifieds')
        except:
            messages.error(request, str(CLASSIFIED_MSG['OOPS']))
            return HttpResponseRedirect(reverse('user_classified_home'))
        
        sp_cost=0
        if classifieds_price_obj.level != 'level0':
            payment_mode=request.POST['payment_mode%d'%(classifieds_price_obj.id)]
       
            period=classifieds_price_obj.contract_period
            if not payment_settings.online_payment or payment_mode=='offline':
                classifieds_obj.listing_start_date=datetime.datetime.now()
                classifieds_obj.listing_end_date=date.today()+relativedelta(months=+period)
                classifieds_obj.status='D'
                classifieds_obj.save()
            
            if classifieds_price_obj.level=='level1':
                if classifieds_obj.category.sp_price:sp_price=classifieds_obj.category.sp_price
                else:sp_price=classifieds_obj.category.parent.sp_price
            elif classifieds_price_obj.level=='level2':
                sp_cost=classifieds_price_obj.price
        else:
            if appreoval_settings.free:
                classifieds_obj.status='P'
                if not classifieds_obj.published_on:classifieds_obj.published_on=datetime.datetime.now()
                try:mail_publish_classifieds(classifieds_obj)
                except:pass
            else:classifieds_obj.status='N'
            classifieds_obj.is_paid=False
            classifieds_obj.price=sp_cost
            classifieds_obj.listing_type='B'
            classifieds_obj.payment=classifieds_price_obj
            classifieds_obj.listing_start_date=datetime.datetime.now()
            classifieds_obj.listing_end_date=date.today()+relativedelta(months=+1)
            classifieds_obj.save()
            ### Notification
            signals.celery_update_index.send(sender=None,object=classifieds_obj)
            notifictn_type = 'posted as '+classifieds_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=classifieds_obj.created_by, obj=classifieds_obj, not_type=notifictn_type,obj_title=classifieds_obj.title)    
            ### Notification
            messages.success(request, str(CLASSIFIED_MSG['CUS']))
            return HttpResponseRedirect(reverse('user_classified_home'))
        
        if not payment_settings.online_payment or payment_mode=='offline':
            classifieds_obj.payment = classifieds_price_obj
            if classifieds_price_obj.level=='level2':classifieds_obj.listing_type='F'
            elif classifieds_price_obj.level=='level1':classifieds_obj.listing_type='S'
            elif classifieds_price_obj.level=='level0':classifieds_obj.listing_type='B'
            classifieds_obj.payment=classifieds_price_obj
            #classifieds_obj.status='N'
            classifieds_obj.is_paid=False
            classifieds_obj.price=sp_cost
            classifieds_obj.save()
            ### Notification
            signals.celery_update_index.send(sender=None,object=classifieds_obj)
            notifictn_type = 'upgraded to '+classifieds_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=classifieds_obj.created_by, obj=classifieds_obj, not_type=notifictn_type,obj_title=classifieds_obj.title)    
            ### Notification
            save_to_paymentorder(request,classifieds_obj,classifieds_price_obj.level_label,sp_cost,classifieds_obj.listing_start_date,classifieds_obj.listing_end_date)
            messages.success(request, str(CLASSIFIED_MSG['CAS']))
            return HttpResponseRedirect(reverse('user_classified_home'))
        
        if payment_settings.online_payment:
            return HttpResponseRedirect(reverse('classifieds_payments_confirm',args=[classifieds_obj.id,classifieds_price_obj.id]))
        
    data['classifieds'] = classifieds_obj
    data['types'] = "update"
    
    if classifieds_obj.category.sp_price:data['sp_price']=classifieds_obj.category.sp_price
    else:data['sp_price']=classifieds_obj.category.parent.sp_price
    data['classifieds_price_objects'] = ClassifiedPrice.objects.filter(level_visibility=True).order_by('id')   
    data['payment_settings']=payment_settings
    return render_to_response(template,data,context_instance = RequestContext(request))


@login_required
def seo(request,id,template='usercp_seo_form.html'):
    classified = Classifieds.objects.get(id = id,created_by=request.user)
    form=UserClassifiedSeoForm(instance=classified)
    if request.POST:
        form=UserClassifiedSeoForm(request.POST,instance=classified)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(CLASSIFIED_MSG['CSUS'])}))
        else:
            data={'form':form,'classified':classified}
            return error_response(request,data,template,CLASSIFIED_MSG)
    data={'form':form,'classified':classified}
    return render_to_response(template,data, context_instance=RequestContext(request))

"""
##################################################################################################################
#####################################   Classifieds ADD/UPDATE     ###############################################
##################################################################################################################
"""

@login_required
def add_classified(request):
    data = {}
    attribute=category=None
    
    try:
        data['classified'] = classified = Classifieds.objects.select_related("category").get(id=int(request.REQUEST['classified']),created_by=request.user)
    except:
        data['classified'] = classified = None
    try:data['category']=category=ClassifiedCategory.objects.select_related("parent").get(id=int(request.POST['sub_category']))
    except:
        if request.method!='POST':
            if classified:data['category']=category=classified.category
            else:data['category']=category=None
    
    if classified:
        form = ClassifiedUserForm(initial = {'action':'B'}, instance=classified)
    else:
        date=datetime.datetime.now()
        formdata={'action':'B'}
        formdata['listing_start_date']=date
        formdata['listing_end_date']=datetime.date.today()+relativedelta( months = +1 )
        form= ClassifiedUserForm(initial=formdata)
    if category:
        cat=[]
        cat.append(category.id)
        cat.append(category.parent.id)
        data['attribute'] = attribute = ClassifiedAttribute.objects.filter(category__id__in=cat ).order_by('-type')
        
    try:
        address=Address.objects.get(id=classified.address.id,status='P')
    except:
        address=None
    if address:
        aform=AddressForm(instance=address)
    else:
        aform=AddressForm()
    if request.POST:
        if classified:form = ClassifiedUserForm(request.POST, instance=classified)
        else:form = ClassifiedUserForm(request.POST)
        if address:
            aform=AddressForm(request.POST, instance=address)
        else:
            aform=AddressForm(request.POST)
        if form.is_valid() and aform.is_valid():
            classified_form = form.save(commit=False)
            classified_form.slug = getUniqueValue(Classifieds,slugify(getSlugData(classified_form.title)))
            classified_form.category = data['category']
            
            classified_form.seo_title = classified_form.title.strip()
            classified_form.seo_description = ds_cleantext(strip_tags(classified_form.description[:250]).strip())
            
            classified_form.created_by =classified_form.modified_by = request.user
            if not classified:
                classified_form.status = 'D'
            
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                if classified and classified.album:
                    album = classified.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = classified_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = classified_form.title
                album.slug = getUniqueValue(PhotoAlbum, slugify(classified_form.slug))
                album.seo_title = classified_form.title[:70],
                album.seo_description = album.summary = classified_form.description[:160]
                album.save()
                
                classified_form.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
            
            address=aform.save(commit=False)
            address = save_classified_address(request, address, classified_form)
            classified_form.address = address 
            classified_form.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=classified_form)
            """
            if classified: 
                if classified.status=='P':
                    if classified.listing_type == 'B':
                        if appreoval_settings.free_update:
                                classified.status='P'
                                if not classified.published_on:
                                    classified.published_on=datetime.datetime.now()
                        else:classified.status='N'
                    else:
                        if appreoval_settings.paid_update:
                            classified.status='P'
                            if not classified.published_on:
                                classified.published_on=datetime.datetime.now()
                        else:classified.status='N'
            else:
                classified_form.status='N'
            classified_form.save()
            if classified_form.status=='P':
                try:mail_publish_classifieds(classified_form)
                except:pass
            """
            select_dict = {}
            if attribute:
                for s in attribute:
                    try:
                        edata = request.POST.getlist('extra_'+str(s.id))
                        if len(edata) > 1:select_dict[s.id] = edata
                        else: select_dict[s.id] = edata[0]
                    except:pass
                    
            save_classified_tags(classified_form, request.POST['tags'])
            #save_classifieds_photos(classified,request.POST.getlist('new_pic'))
            if select_dict:save_classified_attribute(classified_form, select_dict)
            signals.celery_update_index.send(sender=None,object=classified_form)
            if classified:
                if classified_form.status=='P' or classified_form.status=='N':
                    signals.create_staffmail.send(sender=None,object=classified_form,module='classifieds',action='U',user=request.user)
                    return HttpResponseRedirect(reverse('user_classified_home'))
            return HttpResponseRedirect(reverse('user_add_classifieds_listing', args=[classified_form.id]))
            """
            try:
                request.POST['draft']
                classified_form.status ='D'
                classified_form.save()
                messages.success(request, str(CLASSIFIED_MSG['CAS']))
                return HttpResponseRedirect(reverse('user_classified_home'))
            except:
                if classified and classified.status != 'D':
                    ####Update Classified Notification################
                    if classified_form.status=='P' or classified_form.status=='N':
                        signals.create_notification.send(sender=None,user=classified_form.created_by, obj=classified_form, not_type='updated in',obj_title=classified_form.title)
                        signals.create_staffmail.send(sender=None,object=classified_form,module='classifieds',action='U',user=request.user)
                    ##################################################
                    messages.success(request, str(CLASSIFIED_MSG['CUS']))
                    return HttpResponseRedirect(reverse('user_classified_home'))
                else:
                    return HttpResponseRedirect(reverse('user_add_classifieds_listing',args=[classified_form.id]))
            """
    ####################################################################################################################
    data['form'] = form
    data['aform'] = aform
    data['address'] = address
    if request.method=='POST':
        data['new_pic']=request.POST.getlist('new_pic')
        try:data['classifieds_tags'] = request.POST['tags'].split(',')
        except:data['classifieds_tags'] = request.POST['tags']
        try:data['action']=str(request.POST['action'])
        except:pass
    else:
        if classified:data['classifieds_tags']=classified.tags.all()
    
    attr_ids = []
    select_dict = {}
    attribute_dict = []
    if classified or category:
        data['category_list']=ClassifiedCategory.objects.select_related("parent").filter(parent=category.parent)
        if classified:
            sattr = classified.get_attribute_values()
            for sa in sattr:
                attr_ids.append(str(sa.attribute_id.id))
                if sa.attribute_id.type == 'K':select_dict[str(sa.attribute_id.id)] = sa.value.split(',')
                else:select_dict[str(sa.attribute_id.id)] = sa.value
        
        if request.method=='POST':
            attr_ids = []
            if attribute:
                for s in attribute:
                    try:
                        edata = request.POST.getlist('extra_'+str(s.id))
                        if len(edata) > 1: select_dict[str(s.id)] = edata
                        else:select_dict[str(s.id)] = edata[0]
                        attr_ids.append(str(s.id))
                    except:pass
        if attribute:
            for s in attribute:
                w = {'name':s.name, 'id':s.id, 'type':s.type}
                w['default_values'] = s.get_default_values()
        
                x = str(w['id'])
                if x in attr_ids:
                    if select_dict[x]:w['ex_values'] = select_dict[x]
                    else: w['ex_values'] = None
                attribute_dict.append(w)
        
    data['attribute_dict'] =  attribute_dict
    data['classified_price_objects']=ClassifiedPrice.objects.filter(level_visibility=True).order_by('id')
    data['parent_category'] = ClassifiedCategory.objects.filter(parent=None).order_by('name')
    return render_to_response('classifieds/user/classified_form.html',data,context_instance = RequestContext(request))

@login_required
def add_classifieds_listing(request,id):
    data={}
    types = request.REQUEST.get('types','add')
    try:classifieds_obj = Classifieds.objects.get(id = id,created_by=request.user)#,created_by=request.user,status='D'
    except:
        messages.error(request, str(CLASSIFIED_MSG['OOPS']))
        return HttpResponseRedirect(reverse('user_classified_home'))
    payment_settings=PaymentConfigure.get_payment_settings()
    if request.POST :
        try:
            classifieds_price_obj = ClassifiedPrice.objects.get(level = request.POST['payment_level'])
            appreoval_settings = ApprovalSettings.objects.get(name='classifieds')
        except:
            messages.error(request, str(CLASSIFIED_MSG['OOPS']))
            return HttpResponseRedirect(reverse('user_classified_home'))
        
        
        sp_cost=0
        if classifieds_price_obj.level != 'level0':
            payment_mode=request.POST['payment_mode%d'%(classifieds_price_obj.id)]
       
            period=classifieds_price_obj.contract_period
            
            classifieds_obj.listing_start_date=datetime.datetime.now()
            classifieds_obj.listing_end_date=date.today()+relativedelta(months=+period)
            #classifieds_obj.status='N'
            classifieds_obj.save()
            
            for log in classifieds_obj.audit_log.all():
                if log.action_type=='U':
                    log.delete()
                              
            if classifieds_price_obj.level=='level1':
                if classifieds_obj.category.sp_price: sp_cost = classifieds_obj.category.sp_price
                else: sp_cost = classifieds_obj.category.parent.sp_price
            elif classifieds_price_obj.level=='level2':
                sp_cost = classifieds_price_obj.price
        else:
            if appreoval_settings.free:
                classifieds_obj.status='P'
                classifieds_obj.published_on=datetime.datetime.now()
                try:mail_publish_classifieds(classifieds_obj)
                except:pass
            else:classifieds_obj.status='N'
            classifieds_obj.is_paid=False
            classifieds_obj.price=sp_cost
            classifieds_obj.listing_type='B'
            classifieds_obj.payment=classifieds_price_obj
            classifieds_obj.listing_start_date=datetime.datetime.now()
            classifieds_obj.listing_end_date=date.today()+relativedelta(months=+1)
            classifieds_obj.save()
            
            for log in classifieds_obj.audit_log.all():
                if log.action_type=='U':
                    log.delete()
            ### Notification
            signals.celery_update_index.send(sender=None,object=classifieds_obj)
            notifictn_type = 'posted as '+classifieds_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=classifieds_obj.created_by, obj=classifieds_obj, not_type=notifictn_type,obj_title=classifieds_obj.title)    
            if classifieds_obj.status=='P' or classifieds_obj.status=='N':
                signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='A',user=request.user)    
            ### Notification
            messages.success(request, str(CLASSIFIED_MSG['CUS']))
            return HttpResponseRedirect(reverse('user_classified_home'))
        if not payment_settings.online_payment or payment_mode=='offline':
            save_to_offline_payment(
                object=classifieds_obj,
                listing_type={'level0': 'B', 'level1': 'S', 'level2': 'F'}[classifieds_price_obj.level],
                amount=sp_cost,
                email=request.POST['email'],
                phone_no=request.POST['phone_no'],
                address=request.POST['address']
            )
            classifieds_obj.status = 'N'
            classifieds_obj.save()
            messages.success(request, str(CLASSIFIED_MSG['CUS']))
            return HttpResponseRedirect(reverse('user_classified_home'))
        else:
            save_to_offline_payment(
                object=classifieds_obj,
                payment_status='D'
            )
            if classifieds_obj.status == 'N':
                classifieds_obj.status = 'D'
                classifieds_obj.save()
        
        if payment_settings.online_payment:
            classifieds_obj.payment=classifieds_price_obj
            classifieds_obj.save()
            
            for log in classifieds_obj.audit_log.all():
                if log.action_type=='U':
                    log.delete()
                    
            if classifieds_obj.status=='P' or classifieds_obj.status=='N':
                signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='A',user=request.user)    
            return HttpResponseRedirect("%s?types=%s" % (reverse('classifieds_payments_confirm',args=[classifieds_obj.id,classifieds_price_obj.id]),types))
        
    data['classifieds'] = classifieds_obj
    data['types'] = "add"
    try:
        if classifieds_obj.category.sp_price:
            data['sp_price']=classifieds_obj.category.sp_price
        else:
            data['sp_price']=classifieds_obj.category.parent.sp_price
        #data['sp_price']=classifieds_obj.category.parent.sp_price
    except:
        messages.error(request, str(CLASSIFIED_MSG['OOPS']))
        return HttpResponseRedirect(reverse('user_classified_home'))
    data['classifieds_price_objects'] = ClassifiedPrice.objects.filter(level_visibility=True).order_by('id')   
    data['payment_settings']=payment_settings
    return render_to_response('classifieds/user/add_classifieds_listings.html', data, context_instance=RequestContext(request))



@login_required
def update_classified(request,id=None):
    if not id:raise Http404
    data = {}
    attribute=category=None
    
    data['classified'] = classified = Classifieds.objects.select_related("category").get(id=id,created_by=request.user)
    try:data['category']=category=ClassifiedCategory.objects.select_related("parent").get(id=int(request.POST['classified_category']))
    except:data['category']=category=classified.category
    form = EditClassifiedForm(instance=classified)
    cat=[]
    cat.append(category.id)
    cat.append(category.parent.id)
    data['attribute'] = attribute = ClassifiedAttribute.objects.filter(category__id__in=cat ).order_by('-type')
    if request.POST:
        form = EditClassifiedForm(request.POST, instance=classified)
        if form.is_valid():
            appreoval_settings = ApprovalSettings.objects.get(name='classifieds')
            classified = form.save(commit=False)
            classified.slug = getUniqueValue(Classifieds,slugify(getSlugData(classified.title)),instance_pk=classified.id)
            classified.category = data['category']
            classified.seo_title = classified.title.strip()
            classified.seo_description = ds_cleantext(classified.description[:380].strip())
            classified.created_by =classified.modified_by = request.user
            if classified.status=='P':sendsignal=True
            else:sendsignal=False
            
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                if classified and classified.album:
                    album = classified.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = classified_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = classified.title
                album.slug = getUniqueValue(PhotoAlbum, slugify(classified.slug))
                album.seo_title = classified.title[:70],
                album.seo_description = album.summary = classified.description[:160]
                album.save()
                
                classified.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
            
            
            if classified.payment and classified.status=='P':
                if classified.payment.level != 'level0':
                    if appreoval_settings.paid_update:
                        classified.status='P'
                        if not classifieds.published_on:
                            classifieds.published_on=datetime.datetime.now()
                    else:classified.status='N'
                else:
                    if appreoval_settings.free_update:
                        classified.status='P'
                        if not classifieds.published_on:classifieds.published_on=datetime.datetime.now()
                    else:classified.status='N'
            classified.save()
            if sendsignal:signals.create_staffmail.send(sender=None,object=classified,module='classifieds',action='U',user=request.user)
            select_dict = {}
            if attribute:
                for s in attribute:
                    try:
                        edata = request.POST.getlist('extra_'+str(s.id))
                        if len(edata) > 1:select_dict[s.id] = edata
                        else: select_dict[s.id] = edata[0]
                    except:pass
                    
            save_classified_tags(classified, request.POST['tags'])
            #save_classifieds_photos(classified,request.POST.getlist('new_pic'))
            if select_dict:save_classified_attribute(classified, select_dict)
            signals.create_notification.send(sender=None,user=classified.created_by, obj=classified, not_type='updated in',obj_title=classified.title)
            signals.celery_update_index.send(sender=None,object=classifieds)    
            try:
                request.POST['next']
                messages.success(request, str(CLASSIFIED_MSG['CAS']))
                return HttpResponseRedirect(reverse('user_add_classifieds_listing',args=[classified.id])+'?msg=CAS&mtype=s')
            except:
                messages.success(request, str(CLASSIFIED_MSG['CUS']))
                return HttpResponseRedirect(reverse('user_preview_classified',args=[classified.id]))
    ####################################################################################################################
    data['form'] = form
    if request.method=='POST':
        data['new_pic']=request.POST.getlist('new_pic')
        try:data['classifieds_tags'] = request.POST['tags'].split(',')
        except:data['classifieds_tags'] = request.POST['tags']
        try:data['action']=str(request.POST['action'])
        except:pass
    else:
        if classified:data['classifieds_tags']=classified.tags.all()
    
    attr_ids = []
    select_dict = {}
    attribute_dict = []
    
    data['category_list']=ClassifiedCategory.objects.select_related("parent").filter(parent=category.parent)
    if classified:
        sattr = classified.get_attribute_values()
        for sa in sattr:
            attr_ids.append(str(sa.attribute_id.id))
            if sa.attribute_id.type == 'K':select_dict[str(sa.attribute_id.id)] = sa.value.split(',')
            else:select_dict[str(sa.attribute_id.id)] = sa.value
    if request.method=='POST':
        attr_ids = []
        if attribute:
            for s in attribute:
                try:
                    edata = request.POST.getlist('extra_'+str(s.id))
                    if len(edata) > 1: select_dict[str(s.id)] = edata
                    else:select_dict[str(s.id)] = edata[0]
                    attr_ids.append(str(s.id))
                except:pass
    if attribute:
        for s in attribute:
            w = {'name':s.name, 'id':s.id, 'type':s.type}
            w['default_values'] = s.get_default_values()
    
            x = str(w['id'])
            if x in attr_ids:
                if select_dict[x]:w['ex_values'] = select_dict[x]
                else: w['ex_values'] = None
            attribute_dict.append(w)
    data['attribute_dict'] =  attribute_dict
    data['parent_category'] = ClassifiedCategory.objects.filter(parent=None).order_by('name')
    return render_to_response('classifieds/user/classified_form.html',data,context_instance = RequestContext(request))

#return render_to_response('classifieds/user/update_classifieds.html',data,context_instance = RequestContext(request))

@login_required
def ajax_get_user_sub_category(request,template='classifieds/user/part_subcategory.html'):
    data = {}
    data["category_list"]=ClassifiedCategory.objects.select_related("parent").filter(parent__id=int(request.GET['id']))
    try:
        data["classified"]=Classifieds.objects.get(id=int(request.GET["cid"]))
    except:
        pass
    html=render_to_string(template,data,context_instance = RequestContext(request))
    return HttpResponse(simplejson.dumps({'html':html}))

def ajax_get_user_category_attribute(request,template='classifieds/user/part_attributes.html'):
    data={}
    attribute_dict = []
    attr_ids = []
    select_dict={}
    try:classified = Classifieds.objects.select_related("category").get(id=request.GET['cid'])
    except:classified=False
    data['category'] = category=ClassifiedCategory.objects.select_related("parent").get(id=int(request.GET['id']))
    cat=[]
    cat.append(category.id)
    cat.append(category.parent.id)
    data['attribute'] = attribute = ClassifiedAttribute.objects.filter(category__id__in=cat ).order_by('-type')
    if attribute:
        if classified:
            sattr = classified.get_attribute_values()
            for sa in sattr:
                attr_ids.append(str(sa.attribute_id.id))
                if sa.attribute_id.type == 'K':select_dict[str(sa.attribute_id.id)] = sa.value.split(',')
                else:select_dict[str(sa.attribute_id.id)] = sa.value
            
        for s in attribute:
            w = {'name':s.name, 'id':s.id, 'type':s.type}
            w['default_values'] = s.get_default_values()
    
            x = str(w['id'])
            if x in attr_ids:
                if select_dict[x]:w['ex_values'] = select_dict[x]
                else: w['ex_values'] = None

            attribute_dict.append(w)
    data['attribute_dict'] =  attribute_dict
    data['classified']=classified
    html=render_to_string(template,data,context_instance = RequestContext(request))
    return HttpResponse(simplejson.dumps({'html':html,'cat_price':category.parent.sp_price}))


@login_required
def preview_classified(request,id):
    data={}
    data['classified']=classified= Classifieds.objects.get(id=id,created_by=request.user)
    try:data['msg'] =CLASSIFIED_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    return render_to_response('classifieds/user/preview.html',data,context_instance=RequestContext(request))  

@login_required    
def save_to_paymentorder(request,classified,classified_type,featured_price,start_date,end_date):
    po=PaymentOrder(content_object = classified)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Pending'
    po.amount = featured_price
    po.user = request.user
    po.listing_type = classified_type+' Classifieds'
    po.start_date=start_date
    po.end_date=end_date
    po.object_name=classified.get_payment_title()
    po.save()
    return True


