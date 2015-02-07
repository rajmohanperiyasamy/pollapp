import csv
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.encoding import smart_unicode
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

from classifieds.forms import ClassifiedForm, ClassifiedSeoForm, \
    EditClassifiedForm, AddressForm
from classifieds.models import ClassifiedReport, ClassifiedPrice, Address, \
    Classifieds, ClassifiedCategory, ClassifiedAttribute, Tag as ClassifiedTag
from classifieds.tasks import process_classifieds_csv_upload
from classifieds.utils import save_classified_tags, save_classified_attribute, \
    save_classified_address
from common import signals
from common.fileupload import upload_photos_forgallery
from common.getunique import getUniqueValue, getSlugData
from common.mail_utils import mail_publish_classifieds
from common.models import CSVfile, ContactEmails
from common.staff_messages import CLASSIFIED_MSG, COMMON
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name
from common.utils import ds_pagination, ds_cleantext
from common.utilviews import crop_and_save_coverphoto
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from payments.models import PaymentOrder, OfflinePayment
from payments.utils import get_invoice_num


classified_album_cat = PhotoCategory.objects.get_or_create(name="Classifieds", slug='classifieds', is_editable=False)[0]

rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

NO_OF_ITEMS_PER_PAGE=10

"""
###################################################################################################################
############################################    CLASSIFIEDS    ####################################################
###################################################################################################################
"""

@staff_member_required
def list_classified(request,template='classifieds/staff/home.html'):  
    categorys = ClassifiedCategory.objects.select_related("parent").filter(parent__isnull=False).order_by('-parent','name')
    classified = Classifieds.objects.all().select_related('category','created_by').order_by('-created_on')
    classifieds_state = Classifieds.objects.values('status').annotate(s_count=Count('status'))
    
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
    data['category'] = categorys
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['drafted'] =STATE['D']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['expired'] =STATE['E']
    data['search'] =False
    try:data['recent'] = request.GET['pending_classifieds']
    except:data['recent'] = False
    
    try:
        message=request.GET['message']
        message=message.split(',')
        data['msg']= _('Out of %(count1)s classified(s) %(count2)s classified(s) has been added successfully') % {'count1': message[0], 'count2': message[1]}
    except:pass
    
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def ajax_list_classified(request,template='classifieds/staff/ajax_listing.html'):
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


@staff_member_required
def ajax_classified_action(request,template='classifieds/staff/ajax_delete_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    classifieds = Classifieds.objects.filter(id__in=id)
    status=0
    
    if action=='DEL':
        if request.user.has_perm('classifieds.delete_classifieds'):
            signals.celery_delete_indexs.send(sender=None,objects=classifieds)
            for classified in classifieds: 
                try:classified.album.delete()
                except:pass
            classifieds.delete()
            status=1
            msg=str(CLASSIFIED_MSG['CDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('classifieds.publish_classifieds'):
            classifieds.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=classifieds)
            if action=='P':
                classifieds.update(published_on=datetime.datetime.now())
                try:
                    for classified in classifieds:mail_publish_classifieds(classified)
                except:pass
            status=1
            msg=str(CLASSIFIED_MSG['CSCS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    
    for classified in classifieds:
        classified.save()
        for log in classified.audit_log.all()[:1]:
            log.action_type = action
            log.save()
    data=filter_classifieds(request)
    new_id=[]
    
    
    for cs in data['classified']:new_id.append(int(cs.id))
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

   
def filter_classifieds(request):
    key={}
    args = q=()
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
    if listing_type!='all':key['listing_type'] = listing_type
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:args = (~Q(created_by = request.user))
    
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        search_status = request.GET.get('search_status',None)
        
        if search_category:
            categorys = ClassifiedCategory.objects.select_related("parent").get(id=search_category)
            if categorys.parent: key['category'] = categorys
            else:
                categorys = ClassifiedCategory.objects.filter(parent=categorys)
                key['category__in'] = categorys
        
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='desc':key['description__icontains'] = search_keyword
            elif search_type=='postedby':key['created_by__display_name__icontains'] = search_keyword
        
        if search_status:
            key['status'] = search_status
        
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
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    if search:
        data['catgy']= search_category
    data['item_perpage']=item_perpage
    return data 


@staff_member_required
def ajax_classified_state(request,template='classifieds/staff/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
   
    if status == 'all':
        classifieds_state = Classifieds.objects.values('status').annotate(s_count=Count('status'))
    else:
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

@staff_member_required
@permission_required('classifieds.publish_classifieds',raise_exception=True)
def change_status_classified(request):
    try:
        classified = Classifieds.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        classified.status = status
        signals.celery_update_index.send(sender=None,object=classified)
        if status=='P':
            classified.published_on=datetime.datetime.now()
            try:mail_publish_classifieds(classified)
            except:pass
        classified.save()

        for log in classified.audit_log.all()[:1]:
            log.action_type=status
            log.save()
                
        html ='<span title="'+classified.get_status().title()+'" name="'+classified.status+'" id="id_estatus_'+str(classified.id)+'" class="inline-block status-idty icon-'+classified.get_status()+'"></span> '          
        return HttpResponse(html)
    except:
        return HttpResponse('0')
 
"""
##################################################################################################################
#####################################   Classifieds ADD/UPDATE     ###############################################
##################################################################################################################
"""

@staff_member_required
@permission_required('classifieds.add_classifieds',raise_exception=True)
def add_classified(request):
    data = {}
    attribute=category=None
    
    try:data['classified'] = classified = Classifieds.objects.select_related("category").get(id=int(request.REQUEST['classified']))
    except:data['classified'] = classified = None
    try:data['category']=category=ClassifiedCategory.objects.select_related("parent").get(id=int(request.POST['classified_category']))
    except:
        if request.method!='POST':
            if classified:data['category']=category=classified.category
            else:data['category']=category=None
    
    if classified:form = ClassifiedForm(initial = {'action':'B'}, instance=classified)
    else:
        date=datetime.datetime.now()
        formdata={'action':'B'}
        formdata['listing_start_date']=date
        formdata['listing_end_date']=datetime.date.today()+relativedelta( months = +1 )
        form= ClassifiedForm(initial=formdata)
    if category:
        cat=[]
        cat.append(category.id)
        cat.append(category.parent.id)
        data['attribute'] = attribute = ClassifiedAttribute.objects.filter(category__id__in=cat ).order_by('-type')
    aform=AddressForm()
    if request.POST:
        if classified:form = ClassifiedForm(request.POST, instance=classified)
        else:form = ClassifiedForm(request.POST)
        aform=AddressForm(request.POST)
        if form.is_valid() and aform.is_valid():
            classified = form.save(commit=False)
            classified.slug = getUniqueValue(Classifieds,slugify(getSlugData(classified.title)))
            classified.category = category
            
            classified.seo_title = classified.title.strip()
            classified.seo_description = ds_cleantext(strip_tags(classified.description[:250]).strip())
            
            classified.created_by =classified.modified_by = request.user
            
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
            
            classified.save()
            
            address=aform.save(commit=False)
            address = save_classified_address(request, address, classified)
            classified.address = address 
            ####################################PAYMENT####################################
            level_selected = ClassifiedPrice.objects.get(id=int(request.POST.get('listingtype', 1)))
            classified.payment=level_selected
            if level_selected.level != 'level0':
                try:
                    classified.price=int(request.REQUEST['price_'+str(level_selected.id)])
                except:
                    classified.price=int(level_selected.price)
            try:
                classified.listing_start_date = request.POST['listing_start_date']
                classified.listing_end_date =   request.POST['listing_end_date']   
            except:
                classified.listing_start_date = datetime.datetime.now()
                classified.listing_end_date =   datetime.datetime.now()   
                
            if level_selected.level != 'level0':classified.is_paid=True
            else:classified.is_paid=False
            
            classified.save()
            
            if level_selected.level=='level1' or level_selected.level=='level2':
                if level_selected.level=='level1': 
                    classified.listing_type="S"
                    save_to_paymentorder(request,classified,'Sponsored Classified',  classified.price,classified.listing_start_date,classified.listing_end_date)
                elif level_selected.level=='level2':
                    save_to_paymentorder(request,classified,'Featured Classified',  classified.price,classified.listing_start_date,classified.listing_end_date)
                    classified.listing_type="F"
            else:classified.listing_type="B"
            classified.status ='P' 
            classified.published_on=datetime.datetime.now()
            ####################################PAYMENT####################################
            classified.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=classified)
            for log in classified.audit_log.all():
                if log.action_type=='U':
                    log.delete()
            
            select_dict = {}
            if attribute:
                for s in attribute:
                    try:
                        edata = request.POST.getlist('extra_'+str(s.id))
                        if len(edata) > 1:select_dict[s.id] = edata
                        else: select_dict[s.id] = edata[0]
                    except:pass
                    
            save_classified_tags(classified, request.POST['tags'])
            if select_dict:save_classified_attribute(classified, select_dict)
            signals.celery_update_index.send(sender=None,object=classified)
            messages.success(request, str(CLASSIFIED_MSG['CAS']))
            return HttpResponseRedirect(reverse('staff_classified_home'))
    ####################################################################################################################
    data['form'] = form
    data['aform'] = aform
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
    return render_to_response('classifieds/staff/add_classifieds.html',data,context_instance = RequestContext(request))


@staff_member_required
@permission_required('classifieds.change_classifieds',raise_exception=True)
def update_classified(request,id=None):
    if not id:raise Http404
    data = {}
    category=None
    
    data['classified'] = classified = Classifieds.objects.select_related("category").get(id=id)
    try:data['category']=category=ClassifiedCategory.objects.select_related("parent").get(id=int(request.POST['classified_category']))
    except:data['category']=category=classified.category
    
    form = EditClassifiedForm(instance=classified)
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
        form = EditClassifiedForm(request.POST, instance=classified)
        aform=AddressForm(request.POST, instance=address)
        if form.is_valid() and aform.is_valid():
            classified = form.save(commit=False)
            classified.slug = getUniqueValue(Classifieds,slugify(getSlugData(classified.title)),instance_pk=classified.id)
            classified.category = category
            classified.seo_title = classified.title.strip()
            classified.seo_description = ds_cleantext(strip_tags(classified.description[:380]).strip())
            classified.modified_by = request.user
            
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
            classified.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=classified)
            address=aform.save(commit=False)
            address = save_classified_address(request, address, classified)            
            classified.address = address 
            
            select_dict = {}
            if attribute:
                for s in attribute:
                    try:
                        edata = request.POST.getlist('extra_'+str(s.id))
                        if len(edata) > 1:select_dict[s.id] = edata
                        else: select_dict[s.id] = edata[0]
                    except:pass
                    
            save_classified_tags(classified, request.POST['tags'])
            if select_dict:save_classified_attribute(classified, select_dict)
            signals.celery_update_index.send(sender=None,object=classified)
            messages.success(request, str(CLASSIFIED_MSG['CUS']))
            return HttpResponseRedirect(reverse('staff_classified_home'))
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
    
    data['category_list']=ClassifiedCategory.objects.select_related("parent").filter(parent=category.parent)
    if classified:
        sattr = classified.get_attribute_values()
        for sa in sattr:
            attr_ids.append(str(sa.attribute_id.id))
            if sa.attribute_id.type == 'K':select_dict[str(sa.attribute_id.id)] = sa.value.split(',')
            else:select_dict[str(sa.attribute_id.id)] = sa.value
    
    if request.method=='POST':
        attr_ids = []
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
    return render_to_response('classifieds/staff/update_classifieds.html',data,context_instance = RequestContext(request))

@staff_member_required
def preview_classified(request,id):
    data={}
    data['classified'] = Classifieds.objects.get(id=id)
    return render_to_response('classifieds/staff/preview.html',data,context_instance=RequestContext(request))  

@staff_member_required
@permission_required('classifieds.promote_classifieds',raise_exception=True)
def classified_listing_type(request,template='classifieds/staff/ajax_listing_type.html'):
    data={}
    if request.method=='POST':
        ####################################PAYMENT####################################
        data['classified'] = classified = Classifieds.objects.get(id=int(request.POST['id']))
        level_selected = ClassifiedPrice.objects.get(id=request.POST['listingtype'])
        classified.payment=level_selected
        try:classified.price=request.POST['price_'+str(level_selected.id)]
        except:pass
        
        if level_selected.level != 'level0':classified.is_paid=True
        else:classified.is_paid=False
        
        try:
            classified.listing_start_date = request.POST['start_date']
            classified.listing_end_date = request.POST['end_date']  
        except:
            classified.listing_start_date = datetime.datetime.now()
            classified.listing_end_date =   datetime.datetime.now()
        if classified.status == 'E':   
            classified.status = 'P'
        if level_selected.level=='level1' or level_selected.level=='level2':
            if level_selected.level=='level1': 
                classified.listing_type="S"
                save_to_paymentorder(request,classified,'sponsored classified',  classified.price,classified.listing_start_date,classified.listing_end_date)
            elif level_selected.level=='level2':
                save_to_paymentorder(request,classified,'featured classified',  classified.price,classified.listing_start_date,classified.listing_end_date)
                classified.listing_type="F"
        else:classified.listing_type="B"
        #classified.status ='P' 
        if not classified.published_on:classified.published_on=datetime.datetime.now()
        classified.save()
        
        for log in classified.audit_log.all()[:1]:
            if classified.listing_type == 'B':log.action_type = 'N'
            else:log.action_type = classified.listing_type
            log.save()
            
        signals.celery_update_index.send(sender=None,object=classified)
        return HttpResponse(simplejson.dumps({'status':1,'listingtype':classified.listing_type,'id':classified.id,'mtype':get_msg_class_name('s'),'msg':str(CLASSIFIED_MSG['CLUS'])}))
    else:
        data['classified'] = classified = Classifieds.objects.get(id=int(request.GET['id']))
    data['classified_price_objects']=ClassifiedPrice.objects.filter(level_visibility=True).order_by('id')
    return render_to_response(template,data,context_instance = RequestContext(request))


@staff_member_required
@permission_required('classifieds.change_classifieds',raise_exception=True)
def seo(request,id,template='classifieds/staff/update_seo.html'):
    classified = Classifieds.objects.get(id = id)
    form=ClassifiedSeoForm(instance=classified)
    if request.POST:
        form=ClassifiedSeoForm(request.POST,instance=classified)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug = getUniqueValue(Classifieds,slugify(getSlugData(seo.slug)),instance_pk=seo.id)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(CLASSIFIED_MSG['CSUS'])}))
        else:
            data={'form':form,'classified':classified}
            return error_response(request,data,template,CLASSIFIED_MSG)
    data={'form':form,'classified':classified}
    return render_to_response(template,data, context_instance=RequestContext(request))
"""
#################################### Manage Enquires #############################################
"""
@staff_member_required 
def manage_enquiry(request,id,template='common/manage_enquiry.html'):
    page = int(request.GET.get('page',1))
    classified = Classifieds.objects.get(id = id)
    vv = ContentType.objects.get_for_model(classified)
    contacts_list = ContactEmails.objects.filter(content_type=vv,object_id = classified.id)
    data = ds_pagination(contacts_list,page,'contacts_list',NO_OF_ITEMS_PER_PAGE)
    data['sort'] = "-created_on"
    data['module'] = 'classifieds'
    return render_to_response(template,data,context_instance = RequestContext(request))


"""
#####################################################################################################################
######################################################    Abuse    ##################################################
#####################################################################################################################
"""

@staff_member_required
def abuse(request):
    classifieds_report = ClassifiedReport.objects.all()
    ids = []
    for c in classifieds_report:
        ids.append(c.classified.id)
    classifieds = Classifieds.objects.filter(id__in=ids,is_active=True)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    data = ds_pagination(classifieds,page,'classifieds',10)
    data['url'] = '/staff/classifieds/abuse'
    try:
        data['message'] = request.GET['message']
    except:pass
    return render_to_response('classifieds/staff/classifieds-abuse.html',data, context_instance=RequestContext(request))


@staff_member_required
def filter_by(request):
    by = request.GET['filter']
    if by == 'o':
        classifieds_report = ClassifiedReport.objects.filter(report='O')
        message = '%d classifieds filtered by OFFENSIVE'%classifieds_report.count()
    if by == 's':
        classifieds_report = ClassifiedReport.objects.filter(report='S')
        message = '%d classifieds filtered by SPAM'%classifieds_report.count()
    if by == 'd':
        classifieds_report = ClassifiedReport.objects.filter(report='L')
        message = '%d clasifieds filtered by OLD AD'%classifieds_report.count()
    ids = []
    for c in classifieds_report:
        ids.append(c.classified.id)
    classifieds = Classifieds.objects.filter(id__in=ids)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    data = ds_pagination(classifieds,page,'classified',10)
    data['url'] = '/staff/classifieds/abuse'
    data['message'] = message
    return render_to_response('classifieds/staff/classifieds-abuse.html',data, context_instance=RequestContext(request))

@staff_member_required
def bulk_action(request):
    action = request.POST['category']
    ids = request.POST.getlist('trashchecked')
    classifieds_report = ClassifiedReport.objects.filter(id__in=ids)
    classifieds = []
    for report in classifieds_report:
        classifieds.append(report.classified.id)
    classifieds_report = ClassifiedReport.objects.filter(classified__id__in=classifieds)
    if action == 'dlt':
        message = '%d reports have been deleted'%classifieds_report.count()
        classifieds_report.delete()
        url = '/staff/classifieds/abuse/?message='+message
    
    if action == 'dact':
        classifieds_report = Classifieds.objects.filter(id__in=classifieds)
        message = '%d Classified(s) have been deactivated'%classifieds_report.count()
        classifieds_report.update(is_active=False)
        url = '/staff/classifieds/abuse/?message='+message
    
    return HttpResponseRedirect(url)


'''
##################################################################################################################
###########################################  COMMON FUNCTION   ###################################################
##################################################################################################################
'''

@staff_member_required    
def save_to_paymentorder(request,classified,classified_type,featured_price,start_date,end_date):
    po=PaymentOrder(content_object = classified)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Success'
    po.amount = featured_price
    po.user = request.user
    po.listing_type = classified_type
    po.start_date=start_date
    po.end_date=end_date 
    po.object_name=classified.get_payment_title()
    po.save()
    return True


@login_required
def ajax_get_sub_category(request,template='classifieds/ajax_update_classifieds_category.html'):
    category=ClassifiedCategory.objects.select_related("parent").filter(parent__id=int(request.GET['id']))
    html=render_to_string(template,{'category_list':category},context_instance = RequestContext(request))
    return HttpResponse(simplejson.dumps({'html':html}))

@login_required
def ajax_get_category_attribute(request,template='classifieds/ajax_update_classifieds_attribute.html'):
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
def auto_suggest_tag(request):
    try:
        data = ClassifiedTag.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:
        data = ClassifiedTag.objects.all()[:10]
    child_dict = []
    for tag in data :
        buf={'label':tag.tag,'id':tag.id,'value':tag.tag}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), mimetype='application/javascript')


@login_required
def ajax_upload_photos(request):
    if request.method == "POST":
        gal_id = request.POST.get('gal_id')
        aid = request.GET.get('id')
        if gal_id and gal_id.isdigit():
            album = PhotoAlbum.objects.get(id=gal_id)
        elif aid and aid.isdigit():
            classified = Classifieds.objects.get(id=aid)
            album = classified.album
        else: 
            album = None
        response = upload_photos_forgallery(request,Photos,album,'album')
        return response
    else:
        try:
            classified = Classifieds.objects.get(id=request.GET['id'])
            album = classified.album
            return upload_photos_forgallery(request,Photos,album,'album')
        except:
            return HttpResponse('No Object')

# @login_required
# def ajax_get_default_photos(request):  
#     id=request.GET['ids']
#     return get_default_images(request,id,ClassifiedPhoto)\
# 
# 
# @login_required
# def ajax_delete_photos(request,pk):
#     return delete_photos(request,ClassifiedPhoto,pk)


############################Classified Import & Export CSV##########################
ADD_TYPE_VAL = {'S':'SELL','B':'BUY','R':'RENT','O':'RENTOUT'}
LISTINGTYPE_VAL = {'F':'FEATURED','S':'SPONSORED','B':'FREE'}
STATUS_VAL = {'P':'PUBLISHED','N':'PENDING','E':'EXPIRED','R':'REJECTED','B':'BLOCKED','D':'DRAFTED'}

MAX_UPLOAD_FILESIZE = 2097152

@staff_member_required
def classifieds_import_csv(request):
    if request.method=='POST':
        inputfile = request.FILES['classifiedcsv']
        if inputfile.size > MAX_UPLOAD_FILESIZE:
            messages.error(request, "The file is too big, please make sure the size of your file is less than or equals 2Mb!")
            return HttpResponseRedirect(reverse('staff_classifieds_import_csv'))
        else:
            csvfile = CSVfile(
                file=inputfile,
                module='classifieds',
                status='N',
                uploaded_by=request.user
            )
            csvfile.save()
            process_classifieds_csv_upload.delay(csvfile)
            older_files = CSVfile.objects.filter(module='classifieds').order_by('-uploaded_on').values_list('id', flat=True)[5:]
            CSVfile.objects.filter(id__in=older_files).delete()
            messages.success(request, "Your classifieds listings are being added,\nyou will receive notification through email once completed!")
            return HttpResponseRedirect(reverse('staff_classified_home'))
    else:
        data = {
            'filehistory': CSVfile.objects.filter(module='classifieds').order_by('-uploaded_on'),
        }
        return render_to_response('classifieds/staff/import_csv.html', data, context_instance=RequestContext(request))
                

@staff_member_required  
def classifieds_export_csv(request,template='classifieds/staff/export_csv.html'):
    data = {}
    ''' export users records into csv format '''
    if request.method == "POST":
        
        try:data['start_date'] = start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y")
        except:data['start_date'] = start_date = False
        try:data['end_date'] = end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y")
        except:data['end_date'] = end_date = False
        data['order'] = order= request.POST.get('order','-id')
        data['ltype'] = ltype=request.POST.getlist('ltype',None)
        data['status'] = status=request.POST.getlist('status',None)
        data['category']=category=request.POST.getlist('category',None)
        
        key={}
        if start_date and end_date:key['created_on__range']=[start_date,end_date]
        if ltype:key['listing_type__in'] = ltype    
        if status:key['status__in'] = status
        if category:key['category__parent__id__in'] = category
        
        if key:classifieds = Classifieds.objects.filter(**key).order_by(order)
        else:classifieds = Classifieds.objects.all().order_by(order)
        
        if classifieds.count()==0:
            data['categorys'] = ClassifiedCategory.objects.filter(parent__isnull=True).order_by('name')
            data['error_msg'] = _('No records were found for your search. Please try again!')
            return render_to_response (template, data, context_instance=RequestContext(request))
            
        response = HttpResponse(mimetype='text/csv')
        if start_date and end_date:
            sdate=request.POST['start_date'].replace('/','-')
            edate=request.POST['end_date'].replace('/','-')
            file_name='classifieds_'+sdate+'_to_'+edate
        else:file_name='classifieds'
        response['Content-Disposition'] = 'attachment;filename="%s.csv"'%(file_name)
        headers = ['TITLE','DESCRIPTION','PARENT_CATEGORY','SUB_CATEGORY','STATUS','AD_TYPE','TAGS','CLASSIFIED_PRICE','LISTING_TYPE','LISTING_PRICE','LISTING_START_DATE','LISTING_END_DATE','LISTING_IS_PAID','SEO_TITLE','SEO_DESCRIPTION','ADDRESS1','ADDRESS2','PIN','CITY','TELEPHONE','MOBILENO','EMAIL','WEBSITE','LATITUDE','LONGITUDE','ZOOM']    
        writer = csv.writer(response)
        writer.writerow(headers) 
        
        for classified in classifieds:
            tags=','.join([tag.tag for tag in classified.tags.all() if tag.tag])
            ad_type=ADD_TYPE_VAL[classified.action]
            try:listing_type=LISTINGTYPE_VAL[classified.listing_type]
            except:listing_type=LISTINGTYPE_VAL['B']
            status=STATUS_VAL[classified.status]
            classified_price = classified.classified_price if classified.classified_price else 0
            write_data = [classified.title.strip(),classified.description.strip(),classified.category.parent,classified.category,status,ad_type,tags,classified_price,listing_type,classified.price,classified.listing_start_date.strftime('%m/%d/%y') if classified.listing_start_date else "",classified.listing_end_date.strftime('%m/%d/%y') if classified.listing_end_date else "",classified.is_paid,classified.seo_title.encode('utf-8').strip(),classified.seo_description.encode('utf-8').strip()]
            
            address_list = [classified.address.address1,classified.address.address2,classified.address.zip,classified.address.city,classified.address.telephone1,classified.address.mobile,classified.address.email,classified.address.website,classified.address.lat,classified.address.lon,classified.address.zoom]
            write_data.extend(address_list)
            
            write_data = [smart_unicode(text).encode('utf-8', 'ignore') for text in write_data]
            writer.writerow(write_data)
        return response
    
    else:
        data['categorys'] = ClassifiedCategory.objects.filter(parent__isnull=True).order_by('name')
        return render_to_response (template, data, context_instance=RequestContext(request))

def classified_offline_payment(request, cid):
    template = 'payments/staff/process_offline_payment.html'
    obj = Classifieds.objects.get(id=cid)
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
        'submit_url': reverse('classified_offline_payment', args=[obj.id]),
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
                po.amount = payobj.amount
                po.user = obj.created_by
                po.object_name = obj.get_payment_title()
                po.phone_no = payobj.get_value('phone_no')
                po.email = payobj.get_value('email')
                po.offline_mode = request.POST.get('paytype')
                po.cheque_dd_num = request.POST.get('cheque_no')
                
                obj.listing_type = po.listing_type = payobj.get_value('listing_type')
                obj.payment = ClassifiedPrice.objects.get(level={'S': 'level1', 'F': 'level2'}[payobj.get_value('listing_type')])
                obj.published_on = obj.listing_start_date = obj.listing_end_date = po.start_date = po.end_date = datetime.datetime.now()
                
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
                try: mail_publish_classifieds(obj)
                except: pass
            
            return HttpResponse(simplejson.dumps({'status':1}))
    return render_to_response(template,data,context_instance = RequestContext(request))
