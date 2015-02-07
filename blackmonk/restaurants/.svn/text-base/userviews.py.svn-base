import datetime
from datetime import timedelta,date
from dateutil.relativedelta import relativedelta
from time import strptime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils import simplejson
from django.db.models import Q
from django.db.models import Count
from django.db import transaction

from common.fileupload import upload_logo,upload_photos,upload_files,delete_files,delete_photos,upload_pro_cup_photo,delete_pro_cup_photos
from common.templatetags.ds_utils import get_msg_class_name
from common.user_messages import RESTAURAT_MSG
from common.getunique import getUniqueValue,getSlugData
from common.utils import ds_pagination,get_lat_lng
from common.models import ApprovalSettings,PaymentConfigure
from common.mail_utils import mail_publish_restaurant
from common import signals
from locality.models import Venue
from payments.models import PaymentOrder
from payments.utils import get_invoice_num

from restaurants.models import RestaurantCategories, RestaurantLogo, Restaurants, MealTypes, RestaurantFeatures, Cuisines, RestaurantTags, RestaurantAddress, RestaurantWorkingHours, RestaurantMenus, RestaurantImages, RestaurantVideos, RestaurantImages, RestaurantPrice
from restaurants.forms import RestaurantsForm, RestaurantWorkingHoursForm, RestaurantAddressForm, EditRestaurantsForm, RestaurantMenusForm, RestaurantImagesForm, RestaurantSEOForm
from restaurants.adminforms import MealTypesForm
from restaurants.utils import save_restaurant_tags, save_restaurant_logo

status_dict = {
    'Rejected': 'R',
    'Draft': 'D',
    'Published': 'P',
    'Expired': 'E',
    'Pending': 'N',
    'Blocked': 'B',
}
PAY_MONTH_CHOICES = ((1, '1month'),(3, '3month'),(6, '6month'),(12, '1year'),)
NO_OF_ITEMS_PER_PAGE=10
##=========================================================================================================
@login_required
def manage_restaurant(request,template='restaurants/user/home.html'):
    show = request.GET.get('show', None)
    if show is None:
        restaurant = Restaurants.objects.filter(created_by=request.user).select_related('category').order_by('-created_on')
    else:
        restaurant = Restaurants.objects.filter(status=status_dict[show], created_by=request.user).select_related('category').order_by('-created_on')
    restaurant_state = Restaurants.objects.values('status').filter(created_by=request.user).annotate(s_count=Count('status'))
    
    page = int(request.GET.get('page',1))
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    for st in restaurant_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(restaurant, page,'restaurant',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:
        data['msg'] =RESTAURAT_MSG[request.GET['msg']]
    except:
        data['msg'] =None
    try:
        data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:
        data['mtype'] =None
    data['categories'] =  RestaurantCategories.objects.all()
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
def ajax_list_restaurant(request, template='restaurants/user/ajax_listing.html'):
    print "list...res"
    data=filter_search(request)
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
def filter_search(request):
    print "filter.........."
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
    
    key['created_by'] = request.user
    
    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':key['featured_sponsored'] = listing_type
            
            
            
    #....... restaurant searched 
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
         
    
        if search_type=='title':
            key['name__icontains'] = search_keyword
        elif search_type=='description':
            key['description__icontains'] = search_keyword
            
        if search_category:
            key['categories']  = RestaurantCategories.objects.filter(id=search_category)
           
        if search_keyword:
                q =(Q(name__icontains=search_keyword)|Q(categories__name__icontains=search_keyword)|Q(summary__icontains=search_keyword)|Q(description__icontains=search_keyword)|Q(created_by__profile__display_name__icontains=search_keyword))
                if len(args) == 0 :
                    restaurant = Restaurants.objects.filter(~Q(status='D'),q,**key).select_related('categories','created_by').order_by(sort)
                else:
                    restaurant = Restaurants.objects.filter(~Q(status='D'),q,**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :
                restaurant = Restaurants.objects.filter(~Q(status='D'),**key).select_related('categories','created_by').order_by(sort)
            else:
                restaurant = Restaurants.objects.filter(~Q(status='D'),**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :
            restaurant = Restaurants.objects.filter(~Q(status='D'),**key).select_related('categories','created_by').order_by(sort)
        else:
            restaurant = Restaurants.objects.filter(~Q(status='D'),args,**key).select_related('categories','created_by').order_by(sort)
    #....... search done
    
            
    restaurant = restaurant.distinct()
    data = ds_pagination(restaurant,page,'restaurant',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data






def ajax_restaurant_action(request, template='restaurants/user/ajax_delete_listing.html'):
    print "restaurant action......"
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    restaurant = Restaurants.objects.filter(id__in=id,created_by=request.user)
    
    if action=='DEL':
        for bus_del in restaurant:
            signals.create_notification.send(sender=None,user=request.user, obj=bus_del, not_type='deleted from',obj_title=bus_del.name)
        restaurant.delete()
        msg=str(RESTAURAT_MSG['RDS'])
        mtype=get_msg_class_name('s')
    else:
        restaurant.update(status=action)
        msg=str(RESTAURAT_MSG['RSCS'])
        mtype=get_msg_class_name('s')

    data=filter_search(request)
    new_id=[]
    
    for cs in data['restaurant']:new_id.append(int(cs.id))
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
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))




def add_restaurant(request):
    print "add_restaurant........."
    
    date=datetime.datetime.now()
    formdata={'start_date':date,'end_date':datetime.date.today()+relativedelta( months = +1 )}
    form= RestaurantsForm(initial=formdata)
    wform=RestaurantWorkingHoursForm()
    aform=RestaurantAddressForm()
    if request.POST:
        form = RestaurantsForm(request.POST)
        wform=RestaurantWorkingHoursForm(request.POST)
        aform=RestaurantAddressForm(request.POST)
        if form.is_valid() and wform.is_valid() and aform.is_valid():
            restaurant = form.save(commit=False)
            restaurant.slug = getUniqueValue(Restaurants,slugify(getSlugData(request.POST['slug'])))
            restaurant.created_by = restaurant.modified_by = request.user
            restaurant.status='D'
            restaurant.operating_hours=int(request.POST['operating_hours'])
            restaurant.seo_title = restaurant.name
            restaurant.seo_description = strip_tags(restaurant.description[:250])
            
            try:
                restaurant.logo=RestaurantLogo.objects.get(id=int(request.POST['new_pic']))
            except:
                pass
            restaurant.save()
            form.save_m2m()
            
            
            
            if restaurant.operating_hours:
                workinghour=wform.save(commit=False)
                workinghour.status='P'
                workinghour.save()
                restaurant.workinghours=workinghour
                restaurant.save()
                    
            from common.utils import get_global_settings
            global_settings = get_global_settings()
            
            address=aform.save(commit=False)
            address.restaurant=restaurant
            address.status='P' 
            try:
                address.pointer_lat, address.pointer_lng, address.map_zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.map_zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.pointer_lat, address.pointer_lng, address.map_zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            address.save()
            
           
            try:
                files=RestaurantLogo.objects.filter(id=int(request.POST.getlist('new_files')))
                files.update(restaurant=restaurant)
            except:pass
            try:
                request.POST['next']
                messages.success(request, str(RESTAURAT_MSG['RAS']))
                return HttpResponseRedirect(reverse('user_add_restaurant_listing',args=[restaurant.id]))
            except:
                messages.success(request, str(RESTAURAT_MSG['RAS']))
                return HttpResponseRedirect(reverse('user_preview_restaurant',args=[restaurant.id]))
    data={}
    data['form']=form
    data['wform']=wform
    data['aform']=aform
    data['restaurant_price_objects']=RestaurantPrice.objects.filter(level_visibility=True).order_by('id')
    return render_to_response('restaurants/user/add_restaurant.html', data, context_instance=RequestContext(request))




def add_restaurant_listing(request, id):
    print "add_restaurant_listing"
    data={}
    payment_type=None
    try:restaurant_obj = Restaurants.objects.get(id = id,created_by=request.user,status='D')
    except:
        messages.error(request, str(RESTAURAT_MSG['OOPS']))
        return HttpResponseRedirect(reverse('user_manage_restaurant'))
    payment_settings=PaymentConfigure.get_payment_settings()
    if request.POST :
        try:
            restaurant_price_obj = RestaurantPrice.objects.get( level = request.POST['payment_level'])
            appreoval_settings = ApprovalSettings.objects.get(name='restaurants')
        except:
            messages.error(request, str(RESTAURAT_MSG['OOPS']))
            return HttpResponseRedirect(reverse('user_manage_restaurant'))
        
        sp_cost=0
        if restaurant_price_obj.level != 'level0':
            payment_mode=request.POST['payment_mode%d'%(restaurant_price_obj.id)]
            payment_type=request.POST['payment_type']
            
            restaurant_obj.lstart_date=datetime.datetime.now()
            if payment_type == 'Y':restaurant_obj.lend_date=date.today()+relativedelta(years=+1)
            else:restaurant_obj.lend_date=date.today()+relativedelta(months=+1)
            restaurant_obj.save()
            if payment_type=='M':
                if restaurant_price_obj.level=='level1':
                    for b_c in restaurant_obj.categories.all():
                        if b_c.price_month:sp_cost=sp_cost+b_c.price_month
                        else:
                            if b_c.parent_cat.price_month:sp_cost=sp_cost+b_c.parent_cat.price_month
                elif restaurant_price_obj.level=='level2':sp_cost=restaurant_price_obj.price_month
                   
            elif payment_type=='Y': 
                 if restaurant_price_obj.level=='level1':
                    for b_c in restaurant_obj.categories.all():
                        if b_c.price_year:sp_cost=sp_cost+b_c.price_year
                        else:
                            if b_c.parent_cat.price_year:sp_cost=sp_cost+b_c.parent_cat.price_year
                 elif restaurant_price_obj.level=='level2':sp_cost=restaurant_price_obj.price_year
            restaurant_obj.status='N'
        else:
            if not appreoval_settings.free:
                restaurant_obj.status='P'
                try:mail_publish_restaurant(restaurant_obj)
                except:pass
            else:restaurant_obj.status='N'
            restaurant_obj.lstart_date=datetime.datetime.now()
            restaurant_obj.lend_date=date.today()+relativedelta(months=+1)
            restaurant_obj.is_paid=False
            restaurant_obj.sp_cost=sp_cost
            restaurant_obj.featured_sponsored='B'
            restaurant_obj.payment=restaurant_price_obj
            restaurant_obj.payment_type=payment_type
            restaurant_obj.save()
            ### Notification
            notifictn_type = 'listed as '+restaurant_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=request.user, obj=restaurant_obj, not_type=notifictn_type,obj_title=restaurant_obj.name)
            if restaurant_obj.status=='P' or restaurant_obj.status=='N':
                signals.create_staffmail.send(sender=None,object=restaurant_obj,module='restaurants',action='A',user=request.user)    
           ### Notification
            messages.success(request, str(RESTAURAT_MSG['RAS']))
            return HttpResponseRedirect(reverse('user_manage_restaurant'))
        
        if not payment_settings.online_payment or payment_mode=='offline':
            restaurant_obj.payment = restaurant_price_obj
            if restaurant_price_obj.level=='level2':restaurant_obj.featured_sponsored='F'
            elif restaurant_price_obj.level=='level1':restaurant_obj.featured_sponsored='S'
            elif restaurant_price_obj.level=='level0':restaurant_obj.featured_sponsored='B'
            restaurant_obj.payment=restaurant_price_obj
            restaurant_obj.payment_type=payment_type
            restaurant_obj.status='N'
            restaurant_obj.is_paid=False
            restaurant_obj.sp_cost=sp_cost
            restaurant_obj.save()
            ### Notification
            notifictn_type = 'listed as '+restaurant_price_obj.level_label.lower()+' in'
            signals.create_notification.send(sender=None,user=request.user, obj=restaurant_obj, not_type=notifictn_type,obj_title=restaurant_obj.name)
            if restaurant_obj.status=='P' or restaurant_obj.status=='N':
                signals.create_staffmail.send(sender=None,object=restaurant_obj,module='restaurants',action='A',user=request.user)### Notification
            save_to_paymentorder(request,restaurant_obj,restaurant_price_obj.level_label, restaurant_obj.lstart_date, restaurant_obj.lend_date)
            messages.success(request, str(RESTAURAT_MSG['BAS']))
            return HttpResponseRedirect(reverse('user_manage_restaurant'))
        
        if payment_settings.online_payment:
            restaurant_obj.payment=restaurant_price_obj
            restaurant_obj.payment_type=payment_type
            restaurant_obj.save()
            return HttpResponseRedirect(reverse('restaurant_payments_confirm',args=[restaurant_obj.id,restaurant_price_obj.id])+'?type='+str(payment_type))
        
    data['restaurant'] = restaurant_obj
    try:
        for buz_cat in restaurant_obj.categories.all():
            if buz_cat.parent_cat:
                cat=buz_cat.parent_cat
                break
        data['restaurant_cat']=RestaurantCategories.objects.filter(parent_cat=cat)
    except:pass
    s_monthly_price=s_yearly_price=0
    for b_c in restaurant_obj.categories.all():
        if b_c.price_month:s_monthly_price=s_monthly_price+b_c.price_month
        else:
            if b_c.parent_cat.price_month:s_monthly_price=s_monthly_price+b_c.parent_cat.price_month
        
        if b_c.price_year:s_yearly_price=s_yearly_price+b_c.price_year
        else:
            if b_c.parent_cat.price_year:s_yearly_price=s_yearly_price+b_c.parent_cat.price_year
            
    data['s_monthly_price']=s_monthly_price
    data['s_yearly_price']=s_yearly_price
    
    data['restaurant_price_objects'] = RestaurantPrice.objects.filter(level_visibility=True).order_by('id')   
    data['payment_settings']=payment_settings
    return render_to_response('restaurant/user/add_restaurant_listing.html', data, context_instance=RequestContext(request))





def preview_restaurant(request):
    return render_to_response('restaurants/user/test.html', context_instance=RequestContext(request))
    

















def ajax_restaurant_state(request):
    pass



    
    


def update_restaurant(request):
    pass

def seo_restaurant(requets):
    pass



def restaurant_upgrade_listing_type(request):
    pass
#==========================================
def restaurant_menu(request):
    pass

def restaurant_image(request):
    data={}
    data['restaurant']=restaurant= Restaurants.objects.get(id=id,created_by=request.user)
    return render_to_response('restaurants/user/image.html',data,context_instance=RequestContext(request)) 


def restaurant_video(request, id):
    pass
    
    
    
    







