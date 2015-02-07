import string
import random

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.db.models import Q
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model

from common.templatetags.ds_utils import get_msg_class_name,get_status_class
from common.staff_utils import error_response
from common.getunique import getUniqueValue
from common.utils import ds_pagination
from bmshop.products.models import BMProperty,BMPropertyGroup,BMGroupsProperties,ProductPhoto,Manufacturer
from bmshop.products.models import Product,Category,PropertyOption,ProductPropertyValue,BMPAccessories
from bmshop.products.forms import AddPropertyForm,EditPropertyForm,AddPropertyGroupForm,AddProductForm,ProductSeoForm
from bmshop.products.settings import PROPERTY_FILTERIBLE,PROPERTY_DISPLAYBLE,PROPERTY_SELECT_FIELD
from bmshop.products.utils import get_product_key
from bmshop.static_msgs import STAFF_MSG

User = get_user_model()
NO_OF_ITEMS_PER_PAGE=10
NO_OF_PROPERTIES_PER_PAGE=10
NO_OF_GROUPS_PER_PAGE=10



@staff_member_required
def product_list(request,template='bmshop/staff/product_listing.html'):
    product_objs = Product.objects.defer('short_description','description').all().select_related('categories','created_by').order_by('-id')
    product_state = Product.objects.values('status').exclude(status='D').annotate(s_count=Count('status'))
    
    total = 0
    STATE={'P':0,'B':0}
    for st in product_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    data = ds_pagination(product_objs,'1','product_objs',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    data['search'] =False
    
    data['total'] =total
    data['published'] =STATE['P']
    data['blocked'] =STATE['B']
    
    node = Category.tree.all()
    all_node = []
    for n in node:
        if n.is_leaf_node():
            all_node.append(n)
    data['nodes'] = all_node  
    data['manufactures'] = Manufacturer.objects.all().order_by('name')
    return render_to_response (template, data, context_instance=RequestContext(request))

@staff_member_required
def ajax_products(request,template='bmshop/staff/include_product_listing.html'):
    data=filter_products(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    if data['action']:
        send_data['msg'] = data['msg']
        send_data['mtype'] = data['mtype']
    return HttpResponse(simplejson.dumps(send_data))

def filter_products(request):
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
    
    if action:
        try:id=request.GET['ids'].split(',')
        except:id=request.GET['ids']
        action_product = Product.objects.filter(id__in=id)
        if action=='DEL':
            action_product.delete()
            msg=str(STAFF_MSG['SPD'])
            mtype=get_msg_class_name('s')
        else:
            action_product.update(status=action)
            msg=str(STAFF_MSG[action])
            mtype=get_msg_class_name('s')
        
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
        search_manufacture = request.GET.get('man',None)

        if search_category:
            categorys = Category.objects.get(id=search_category)
            key['categories'] = categorys
        if search_type:
            if search_type=='name':key['name__icontains'] = search_keyword
            elif search_type=='manu':key['manufacturer__name__icontains'] = search_keyword
            else:key['created_by__profile__display_name__icontains'] = search_keyword
        if search_manufacture:
            manufacture = Manufacturer.objects.get(id=search_manufacture)
            key['manufacturer'] = manufacture
                
        if search_keyword:
            q =(Q(name__icontains=search_keyword)|Q(uid__icontains=search_keyword)|Q(categories__name__icontains=search_keyword)|Q(manufacturer__name__icontains=search_keyword)|Q(created_by__profile__display_name__icontains=search_keyword))
            if not created_user:product_objs = Product.objects.defer('short_description','description').filter(~Q(status='D'),q,**key).select_related('categories','created_by').order_by(sort)
            else:product_objs = Product.objects.defer('short_description','description').filter(~Q(status='D'),q,**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if not created_user:product_objs = Product.objects.defer('short_description','description').filter(~Q(status='D'),**key).select_related('categories','created_by').order_by(sort)
            else:product_objs = Product.objects.defer('short_description','description').filter(~Q(status='D'),**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)

    else:
        if not created_user:product_objs = Product.objects.defer('short_description','description').filter(~Q(status='D'),**key).select_related('categories','created_by').order_by(sort)
        else:product_objs = Product.objects.defer('short_description','description').filter(~Q(status='D'),**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)


    data = ds_pagination(product_objs,page,'product_objs',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    data['action']=action
    if action:
        data['msg'] = msg
        data['mtype'] = mtype
    return data

@staff_member_required
def ajax_products_state(request):
    status = request.GET.get('status','all')
    total = 0
    STATE={'P':0,'B':0}

    if status == 'all':
        product_state = Product.objects.values('status').exclude(status='D').annotate(s_count=Count('status'))
    else:
        product_state = Product.objects.filter(created_by=request.user).values('status').exclude(status='D').annotate(s_count=Count('status'))

    for st in product_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'blocked':STATE['B']
    }
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
def preview_product(request,product_id,template='bmshop/staff/preview.html'):
    try:product_obj=Product.objects.get(id=product_id)
    except:
        messages.error(request, str(STAFF_MSG['OOPS']))
        return HttpResponseRedirect(reverse('staff_bmshop_product_list'))
        
    
    
    displayables,is_displayables = get_displayables_properties(request,product_obj)
    
    
    data = {'pty_obj':product_obj,'displayables':displayables,
                   'is_displayables':is_displayables,'is_group':product_obj.property_groups.all()}
    
    return render_to_response (template, data, context_instance=RequestContext(request))

@staff_member_required
def add_product(request,product_id=None,template='bmshop/staff/add_product.html'):
    product_obj = None
    new_pic = None
    default_pic = None
    old_product_id = ""
    clone = ""
    accessories=[]
    try:
        product_obj=Product.objects.get(id=product_id)
        form = AddProductForm(instance=product_obj)
        default_pic = product_obj.get_default_photo()
    except:
        form = AddProductForm()

    if request.method =='POST':
        if product_obj:
            form=AddProductForm(request.POST,instance=product_obj)
            new_uid = False
        else:
            form=AddProductForm(request.POST)
            new_uid = True
        
        new_pic=request.POST.getlist('new_pic')
        default_pic = request.POST['default_img']
        accessories = request.POST.getlist('accessories')
        is_clone = bool(request.POST['is_clone'])
        if is_clone:
            old_product_id = request.POST.get('old_product','')
            clone = "YES"

        if form.is_valid():
            product_obj = form.save(commit=False)
            try:slug = request.POST['slug'].strip()
            except:slug = product_obj.name
            product_obj.slug=getUniqueValue(Product,slugify(slug),instance_pk=product_obj.id)
            product_obj.created_by = request.user
            product_obj.static_price  = form.cleaned_data['price']
            product_obj.status = 'P'
            product_obj.save()
            form.save_m2m()
            if new_pic:
               product_photos = ProductPhoto.objects.filter(id__in=new_pic)
               for product_photo in product_photos:
                   if default_pic:
                       if product_photo.id == int(default_pic):
                           product_photo.default = True
                       else:
                            product_photo.default = False
                   if is_clone:
                       product_photo.pk = None
                   product_photo.product = product_obj
                   product_photo.title = product_obj.name
                   product_photo.save()
            
            
            BMPAccessories.objects.filter(product=product_obj).delete()
            if accessories:
                for accessory in accessories:
                    accessory_obj = Product.objects.get(id=accessory)
                    BMPAccessories.objects.create(product=product_obj,accessory=accessory_obj)
            
            if new_uid:
                try:
                    cat = product_obj.get_category()[0]
                    p_uid = get_product_key(cat.name)
                except:
                    p_uid = get_product_key()
                product_obj.uid = p_uid    
            
            product_obj.meta_title = product_obj.name
            product_obj.meta_description = strip_tags(product_obj.description[:250]).strip() 
            product_obj.save()
            
            if is_clone:
                _clone_properties(old_product_id,product_obj)
                
            submit_type = request.POST['finish_button']
            
            messages.success(request, str(STAFF_MSG['GAS']))
            if submit_type == 'next':
                return HttpResponseRedirect(reverse('staff_bmshop_product_property',args=[product_obj.id]))      
            else:
                return HttpResponseRedirect(reverse('staff_bmshop_product_list'))
    
    if product_obj:product_objs = Product.objects.only('name').exclude(id=product_obj.id).order_by('-id')   
    else:product_objs = Product.objects.only('name').order_by('-id')                 
    
    data = {
            'form':form,
            'product_obj':product_obj,
            'new_pic':new_pic,
            'default_pic':default_pic,
            'product_objs':product_objs,
            'old_id':old_product_id,
            'clone':clone
        }
    return render_to_response (template, data, context_instance=RequestContext(request))

@staff_member_required
def clone_product(request,product_id,template='bmshop/staff/add_product.html'):
    product_obj=Product.objects.get(id=product_id)
    form = AddProductForm(instance=product_obj)
    data = {'product_obj':product_obj,'form':form,'clone':'YES','old_id':product_obj.id}
    
    return render_to_response (template, data, context_instance=RequestContext(request))

@staff_member_required
def product_property(request,product_id=None,template='bmshop/staff/product_property.html'):
    try:
        product_obj=Product.objects.get(id=product_id)
    except:
        messages.error(request, str(STAFF_MSG['OOPS']))
        return HttpResponseRedirect(reverse('staff_bmshop_product_list'))
        
    data = {'product_obj':product_obj,'group_objs':BMPropertyGroup.objects.all()}
    return render_to_response (template, data, context_instance=RequestContext(request))

def _clone_properties(old_product_id,new_product):
    try:
        old_product=Product.objects.get(pk=int(old_product_id))
    
        for group_obj in old_product.property_groups.all():
            for property in group_obj.properties.filter().order_by("bmgroupsproperties"):
                pty_values = ProductPropertyValue.objects.filter(property=property,group=group_obj,product=old_product)
                for pty_value in pty_values:
                    pty_value.pk = None
                    pty_value.product = new_product
                    pty_value.save()
            group_obj.products.add(new_product)
    except:pass    
        
def get_displayables_properties(request,product_obj):
    displayables = []
    is_displayables = False
    
    for group_obj in product_obj.property_groups.all().order_by('position'):
        properties = []
        for property in group_obj.properties.filter().order_by("bmgroupsproperties"):
            is_displayables = True

            ppvs = ProductPropertyValue.objects.filter(property=property,group=group_obj,product=product_obj, type=PROPERTY_DISPLAYBLE)
            value_ids = [ppv.value for ppv in ppvs]

            options = []
            for option in property.options.all():

                if str(option.id) in value_ids: selected = True
                else:selected = False
                options.append({ "id": option.id,"name": option.name,"selected": selected, })

            value = ""
            if property.type == PROPERTY_SELECT_FIELD:
                display_select_field = True
            else:
                display_select_field = False
                try:
                    value = value_ids[0]
                except IndexError:pass

            properties.append({"id": property.id,"name": property.name,"title": property.title,
                 "type": property.type,"options": options,"value": value,
                "display_text_field": not display_select_field,"display_select_field": display_select_field, })
       
        displayables.append({"id": group_obj.id, "name": group_obj.name, "properties": properties, })
        
    return displayables,is_displayables    

@staff_member_required
def ajax_get_property(request,template='bmshop/staff/ajax_retrive_group.html'):
    try:product_obj=Product.objects.get(id=request.POST['pid'])
    except:pass
    
    selected_group_ids = request.POST.getlist("group_ids")
    for group_obj in BMPropertyGroup.objects.all():
        if str(group_obj.id) in selected_group_ids:
            try:
                group_obj.products.get(pk=product_obj.id)
            except:
                group_obj.products.add(product_obj.id)
        else:
            group_obj.products.remove(product_obj.id)
    
    displayables,is_displayables = get_displayables_properties(request,product_obj)
    
    
    append_data = {'product_obj':product_obj,'displayables':displayables,
                   'is_displayables':is_displayables,'is_group':product_obj.property_groups.all()}
    
    include_html=render_to_string(template,append_data,context_instance=RequestContext(request))
    data = {'html':include_html,'status':1}
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
@require_POST
def update_product_properties(request,product_id):
    type = 1
    ProductPropertyValue.objects.filter(product=product_id, type=type).delete()

    for key in request.POST.keys():
        if key.startswith("property") == False:
            continue
        try:
            property_id = key.split("-")[1]
            group_id = key.split("-")[2]
            property = get_object_or_404(BMProperty, pk=property_id)
            group = get_object_or_404(BMPropertyGroup, pk=group_id)
            product = get_object_or_404(Product, pk=product_id)
    
            for value in request.POST.getlist(key):
                if property.is_valid_value(value):
                    ProductPropertyValue.objects.create(product=product, property=property,group=group,value=value, type=type)
        except:
            pass    
    messages.success(request, str(STAFF_MSG['GAS']))           
    return HttpResponseRedirect(reverse('staff_bmshop_product_list'))
    
    
@staff_member_required
def feature_product(request):
    try:
        product=Product.objects.only("featured").get(id=int(request.GET['id']))
        featured = request.GET['status']
        if featured == 'F':
            product.featured = True
        else:
            product.featured = False
        product.save()
        return HttpResponse('1')
    except:return HttpResponse('0')

@staff_member_required
def change_status(request):
    try:
        product=Product.objects.only('status').get(id=int(request.GET['id']))
        status = request.GET['status']
        product.status = status
        product.save()
        html ='<span title="'+get_status_class(product.status)+'" name="'+product.status+'" id="id_estatus_'+str(product.id)+'" class="inline-block status-idty icon-'+get_status_class(product.status)+'"></span> '
        return HttpResponse(html)
    except:return HttpResponse('0')

@staff_member_required
def seo(request,id,template='bmshop/staff/update_seo.html'):
    product = Product.objects.only('meta_title','meta_description').get(id=id)
    form=ProductSeoForm(instance=product)
    if request.POST:
        form=ProductSeoForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(STAFF_MSG['SEO'])}))
        else:
            data={'form':form,'product':product}
            return error_response(request,data,template,STAFF_MSG)
    data={'form':form,'product':product}
    return render_to_response(template,data, context_instance=RequestContext(request))
   
from common.fileupload import upload_photos,delete_photos,get_default_images
@staff_member_required
def ajax_upload_photos(request):  
    try:product = Product.objects.get(id=request.GET['id'])
    except:product=None
    return upload_photos(request,ProductPhoto,product,'product')

@staff_member_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,ProductPhoto,pk)

@staff_member_required
def ajax_get_default_photos(request):  
    id=request.GET['ids']
    return get_default_images(request,id,ProductPhoto)



############################## MANAGE PROPERTY ##########################################
@staff_member_required
def property_list(request,template='bmshop/staff/property_listing.html'):
    prpty_objs = BMProperty.objects.order_by('-created_on')
    data = ds_pagination(prpty_objs,'1','prpty_objs',NO_OF_PROPERTIES_PER_PAGE)
    data['sort']='-created_on'
    data['search'] =False
    return render_to_response (template, data, context_instance=RequestContext(request))

@staff_member_required
def ajax_property(request,template='bmshop/staff/include_property_listing.html'):
    data=filter_property(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    if data['is_delete']:
        if data['delete_status']:
            send_data['msg']=str(STAFF_MSG['PSD'])
            send_data['mtype']=get_msg_class_name('s')
        else:
            send_data['msg']=str(STAFF_MSG['OOPS'])
            send_data['mtype']=get_msg_class_name('e')        
    return HttpResponse(simplejson.dumps(send_data))

def filter_property(request):
    data=key={}
    q=()
    delete_status = False
    sort = request.GET.get('sort','-created_on')
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_PROPERTIES_PER_PAGE))
    page = int(request.GET.get('page',1))
    is_delete = request.GET.get('del',False)
    if is_delete:
        try:
            BMProperty.objects.get(id=request.GET['did']).delete()
            delete_status = True
        except:delete_status = False
        
    if search:
        search_keyword = request.GET.get('kwd',None).strip()
        if search_keyword:
            prpty_objs = BMProperty.objects.filter(name__icontains=search_keyword).select_related('groups','products').order_by(sort)
        else:
            prpty_objs = BMProperty.objects.all().select_related('groups','products').order_by(sort)
    else:
        prpty_objs = BMProperty.objects.all().select_related('groups','products').order_by(sort)

    data = ds_pagination(prpty_objs,page,'prpty_objs',item_perpage)
    data['sort']= sort
    data['is_delete'] = is_delete
    data['delete_status'] = delete_status
    data['search']= search
    data['item_perpage']=item_perpage
    return data

@staff_member_required
def add_property(request,property_id=None,template='bmshop/staff/add_property.html'):
    select_options = None
    try:
        pty_obj = BMProperty.objects.get(id=property_id)
        form = EditPropertyForm(instance=pty_obj)
        if pty_obj.is_select_field():select_options=pty_obj.get_property_option()
    except:
        pty_obj = None
        form = AddPropertyForm()    
    
    if request.method == "POST":
        if pty_obj:form=EditPropertyForm(request.POST,instance=pty_obj)
        else:form=AddPropertyForm(request.POST)
        select_options=request.POST.getlist('select_field_opt')
        if form.is_valid():
            pty_obj = form.save(commit=False)
            pty_obj.created_by = request.user
            pty_obj.save()
            if int(form.cleaned_data['type'])==2:
                PropertyOption.objects.filter(property=pty_obj.id).delete()
                for name in select_options:
                    PropertyOption.objects.get_or_create(property=pty_obj,name=name)
                    
            messages.success(request, str(STAFF_MSG['PUS'])) 
            return HttpResponseRedirect(reverse('staff_bmshop_property_list'))
    data = {'form':form,'pty_obj':pty_obj,'select_options':select_options}
    return render_to_response (template, data, context_instance=RequestContext(request))


################################## MANAGE GROUP PROPERTY #########################################
@staff_member_required
def group_property_list(request,template='bmshop/staff/group_property_listing.html'):
    group_objs = BMPropertyGroup.objects.order_by('-created_on')
    data = ds_pagination(group_objs,'1','group_objs',NO_OF_GROUPS_PER_PAGE)
    data['sort']='-created_on'
    data['search'] =False
    return render_to_response (template, data, context_instance=RequestContext(request))

@staff_member_required
def ajax_group(request,template='bmshop/staff/include_property_grplisting.html'):
    data=filter_group(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    if data['is_delete']:
        if data['delete_status']:
            send_data['msg']=str(STAFF_MSG['PGD'])
            send_data['mtype']=get_msg_class_name('s')
        else:
            send_data['msg']=str(STAFF_MSG['OOPS'])
            send_data['mtype']=get_msg_class_name('e')            
    return HttpResponse(simplejson.dumps(send_data))

def filter_group(request):
    data=key={}
    q=()
    delete_status = False
    sort = request.GET.get('sort','-created_on')
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_GROUPS_PER_PAGE))
    page = int(request.GET.get('page',1))
    is_delete = request.GET.get('del',False)
    if is_delete:
        try:
            BMPropertyGroup.objects.get(id=request.GET['did']).delete()
            delete_status = True
        except:delete_status = False
    
    if search:
        search_keyword = request.GET.get('kwd',None).strip()
        if search_keyword:
            group_objs = BMPropertyGroup.objects.filter(name__icontains=search_keyword).select_related('products').order_by(sort)
        else:
            group_objs = BMPropertyGroup.objects.all().select_related('products').order_by(sort)
    else:
        group_objs = BMPropertyGroup.objects.all().select_related('products').order_by(sort)


    data = ds_pagination(group_objs,page,'group_objs',item_perpage)
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    data['is_delete'] = is_delete
    data['delete_status'] = delete_status
    return data

@staff_member_required
def add_property_group(request,template='bmshop/staff/lb_add_property_group.html'):
    try:
        group_obj = BMPropertyGroup.objects.get(id=request.REQUEST['id'])
        form = AddPropertyGroupForm(instance=group_obj)
        group_property_obj = BMGroupsProperties.objects.filter(group_id=group_obj.id)
    except:
        group_obj = None
        group_property_obj = None
        form = AddPropertyGroupForm()    
    prpty_objs = BMProperty.objects.order_by('name')
    if request.method == "POST":
        if group_obj:form=AddPropertyGroupForm(request.POST,instance=group_obj)
        else:form=AddPropertyGroupForm(request.POST)
        if form.is_valid():
            group_obj = form.save(commit=False)
            group_obj.created_by = request.user
            group_obj.save()
            BMGroupsProperties.objects.filter(group_id=group_obj.id).delete()
            for property_id in request.POST.getlist('properties'):
                try:
                    BMGroupsProperties.objects.create(group_id=group_obj.id, property_id=property_id)
                except IntegrityError:
                    pass
            
            send_data={'status':1,'msg':str(STAFF_MSG['PGS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(send_data))
        else:
            lightbox_html=render_to_string(template,
                        {'form':form,'group_obj':group_obj,'prpty_objs':prpty_objs},
                        context_instance=RequestContext(request))
            send_data={'lightbox_html':lightbox_html,'status':0}
            return HttpResponse(simplejson.dumps(send_data))
    
    data = {'form':form,'group_obj':group_obj,'prpty_objs':prpty_objs,'group_property_obj':group_property_obj}
    return render_to_response (template, data, context_instance=RequestContext(request))
   

