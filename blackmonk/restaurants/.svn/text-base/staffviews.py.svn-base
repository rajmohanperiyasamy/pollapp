import csv
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from time import strptime
import urllib2
from googlemaps import GoogleMaps

from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils import simplejson
from django.db.models import Q
from django.db.models import Count
from django.core.files.temp import NamedTemporaryFile
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.db import transaction
from django.contrib import messages

from common.fileupload import upload_logo,upload_photos,upload_files,delete_files,delete_photos,upload_pro_cup_photo,delete_pro_cup_photos
from common.templatetags.ds_utils import get_msg_class_name
from common.staff_messages import RESTAURANT_MSG,COMMON
from common.getunique import getUniqueValue,getSlugData
from common.mail_utils import mail_publish_restaurant
from common.utils import ds_pagination,get_lat_lng

from locality.models import Venue
from payments.models import PaymentOrder
from payments.utils import get_invoice_num
from common import signals

NO_OF_ITEMS_PER_PAGE=10
PAY_MONTH_CHOICES = ((1, '1month'),(3, '3month'),(6, '6month'),(12, '1year'),)

from restaurants.models import RestaurantCategories, RestaurantLogo, Restaurants, MealTypes, RestaurantFeatures, Cuisines, RestaurantTags, RestaurantAddress, RestaurantWorkingHours, RestaurantMenus, RestaurantImages, RestaurantVideos, RestaurantImages, RestaurantPrice
from restaurants.forms import RestaurantsForm, RestaurantWorkingHoursForm, RestaurantAddressForm, EditRestaurantsForm, RestaurantMenusForm, RestaurantImagesForm, RestaurantSEOForm
from restaurants.adminforms import MealTypesForm
from restaurants.utils import save_restaurant_tags, save_restaurant_logo







#============================================= helper methods
@login_required
def ajax_upload_logo(request):
    try:
        restaurant = Restaurants.objects.get(id=int(request.GET['id']))
    except:
        restaurant=None
    return upload_logo(request, RestaurantLogo, restaurant)

@login_required
def restaurant_delete_logo(request,pk):
    return delete_photos(request, RestaurantLogo, pk)


@staff_member_required
def auto_suggest_tag(request):
    try:
        data = RestaurantTags.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:
        data = RestaurantTags.objects.all()[:10]
    child_dict = []
    for tag in data :
        buf={'label':tag. tag,'id':tag.id, 'value':tag.tag}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), mimetype='application/javascript')


@staff_member_required
def save_to_paymentorder(request,restaurant,restaurant_type,start_date,end_date):
    po=PaymentOrder(content_object = restaurant)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Success'
    po.user = request.user
    po.listing_type = str(restaurant_type)+' Restaurant'
    po.start_date=start_date
    po.end_date=end_date
    po.save()
    return True

#.............................................

@staff_member_required
def manage_restaurant(request,template='restaurants/staff/home.html'):
    restaurants = Restaurants.objects.filter(~Q(status='D')).select_related('category','created_by').order_by('-created_on')
    restaurant_state = Restaurants.objects.values('status').annotate(s_count=Count('status')).exclude(status='D')

    page = int(request.GET.get('page',1))
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    for st in restaurant_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']

    data = ds_pagination(restaurants, page,'restaurants', NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =RESTAURANT_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None

    try:
        message=request.GET['message']
        message=message.split(',')
        data['msg']= _('Out of %(count1)s restaurant %(count2)s restaurant has been added successfully') % {'count1': message[0], 'count2': message[1]}
    except:pass

    data['categories'] = RestaurantCategories.objects.all()
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['search'] =False
    try:data['recent'] = request.GET['pending_restaurant']
    except:data['recent'] = False
    return render_to_response(template,data, context_instance=RequestContext(request))

############################################# RESTAURANT ADD ###############################################################

#@transaction.commit_on_success
@staff_member_required
@permission_required('restaurants.add_restaurants',raise_exception=True)
def add_restaurant(request):
    if request.method == "POST":
        form  = RestaurantsForm(request.POST)
        wform = RestaurantWorkingHoursForm(request.POST)
        aform = RestaurantAddressForm(request.POST)   
       
        if form.is_valid() and aform.is_valid() and wform.is_valid():
            #---------- saving RestaurantsForm
            restaurant = form.save(commit=False)
            restaurant.created_by=restaurant.modified_by=request.user
            restaurant.operating_hours=int(request.POST['operating_hours'])
            restaurant.slug = getUniqueValue(Restaurants,slugify(getSlugData(request.POST['slug'])))
            restaurant.seo_title=request.POST['name']
            restaurant.seo_description=strip_tags(restaurant.description[:250]).strip()
            restaurant.start_date = request.POST['start_date']
            restaurant.end_date =   request.POST['end_date']
                
            draft=request.POST.get('draft',False)     
            if not draft:
                restaurant.status='P'
            else:
                restaurant.status='N'
            restaurant.save()
            form.save_m2m()
            
            #. saving tags
            save_restaurant_tags(request.POST['tags'],restaurant)
            
            #..... saving logo
            try:
                logo_obj = RestaurantLogo.objects.get(id=int(request.POST['new_pic']))
                restaurant.logo = logo_obj
                restaurant.save()
            except:
                pass
            
            
            #................ saving pricing info
            listing_type = RestaurantPrice.objects.get(id=int(request.POST['listingtype']))
            if listing_type.level=='level2':
                restaurant.featured_sponsored="F"
                pass
            elif listing_type.level=='level1':
                restaurant.featured_sponsored="S"
            else:
                restaurant.featured_sponsored="B"
            
            if listing_type!="level0":
                restaurant.is_paid=True
                restaurant.payment_type=request.POST['period']
                save_to_paymentorder(request, restaurant, listing_type.level_label, restaurant.start_date, restaurant.end_date)
            else:
                restaurant.is_paid=False
                
            restaurant.payment=listing_type
            restaurant.save()
          
            
            
            
            #---------- saving RestaurantWorkingHoursForm
            if restaurant.operating_hours:
                workinghours=wform.save(commit=False)
                workinghours.status='P'
                workinghours.save()
                restaurant.workinghours=workinghours
                restaurant.save()
                wform.save()
            
            
            #---------- saving RestaurantAddressForm
            from common.utils import get_global_settings
            global_settings = get_global_settings()
            
            address=aform.save(commit=False)
            address.restaurant=restaurant
            address.status='P'
            try:
                address.pointer_lat, address.pointer_lng, address.map_zoom = get_lat_lng(request.POST['lat_lng'])
                try:
                    address.map_zoom = int(request.POST['zoom'])
                    #print "............ try" ,address.pointer_lat, address.pointer_lng, address.map_zoom
                except:
                        pass#print " exp..........."
            except:
                address.pointer_lat, address.pointer_lng, address.map_zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
                #print "except............" ,address.pointer_lat, address.pointer_lng, address.map_zoom
            address.save()
            aform.save_m2m()
            signals.celery_update_index.send(sender=None,object=restaurant)
            

            
            
            
            #-------response
            messages.success(request, str(RESTAURANT_MSG['YAS']))
            return HttpResponseRedirect(reverse('staff_preview_restaurant',args=[restaurant.id]))
        else:
            print "not valid...form", form.errors
            print "not valid....wform", wform.errors
            print "not valid....aform", aform.errors
    
    else:
        data={}
        formdata={'start_date': datetime.datetime.now(),'end_date': datetime.date.today()+relativedelta( months = +1 )}
        data['form']= RestaurantsForm(initial=formdata)
        data['wform']=RestaurantWorkingHoursForm()
        data['aform']=RestaurantAddressForm()
        data['restaurant_price_objects']=RestaurantPrice.objects.filter(level_visibility=True).order_by('id')
        return render_to_response('restaurants/staff/add_restaurant.html',data, context_instance=RequestContext(request))




@staff_member_required
def preview_restaurant(request,id):
    data={}
    data['restaurant']=restaurant= Restaurants.objects.prefetch_related('restaurant_address').get(id=id)
   
    try:data['msg'] =RESTAURANT_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    return render_to_response('restaurants/staff/preview.html',data,context_instance=RequestContext(request))



@staff_member_required
@permission_required('restaurants.change_restaurants',raise_exception=True)
def update_restaurant(request, id):
    print"update...."
    restaurant=Restaurants.objects.get(id=id)
    try:
        whour=RestaurantWorkingHours.objects.get(id=restaurant.workinghours.id)
    except:
        whour=None
    try:
        address=RestaurantAddress.objects.get(restaurant=restaurant)
        
    except:
        address=None

    form= EditRestaurantsForm(instance=restaurant)
    wform=RestaurantWorkingHoursForm(instance=whour)
    aform=RestaurantAddressForm(instance=address)
    
    
    if request.method=='POST':
        print "post..."
        form = EditRestaurantsForm(request.POST, instance=restaurant)
        wform=RestaurantWorkingHoursForm(request.POST, instance=whour)
        aform=RestaurantAddressForm(request.POST, instance=address)
        
        if form.is_valid() and wform.is_valid() and aform.is_valid():
            print "valid.....", 
            restaurant = form.save(commit=False)
            restaurant.created_by=restaurant.modified_by=request.user
            restaurant.status='P'
            restaurant.operating_hours=int(request.POST['operating_hours'])
            restaurant.save()
            form.save_m2m()
            #. saving tags
            save_restaurant_tags(request.POST['tags'],restaurant)
            
            #..... saving logo
            try:
                logo_obj = RestaurantLogo.objects.get(id=int(request.POST['new_pic']))
                restaurant.logo = logo_obj
                restaurant.save()
            except:
                pass

            
             #---------- saving RestaurantWorkingHoursForm
            if restaurant.operating_hours:
                workinghours=wform.save(commit=False)
                workinghours.status='P'
                workinghours.save()
                restaurant.workinghours=workinghours
                restaurant.save()
                wform.save()

            #---------- saving RestaurantAddressForm
            from common.utils import get_global_settings
            global_settings = get_global_settings()
            
            address=aform.save(commit=False)
            address.restaurant=restaurant
            address.status='P'
            try:
                address.pointer_lat, address.pointer_lng, address.map_zoom = get_lat_lng(request.POST['lat_lng'])
                try:
                    address.map_zoom = int(request.POST['zoom'])
                    print "............ try" ,address.pointer_lat, address.pointer_lng, address.map_zoom
                except:
                    print " exp..........."
            except:

                address.pointer_lat, address.pointer_lng, address.map_zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
                print "except............" ,address.pointer_lat, address.pointer_lng, address.map_zoom
            address.save()
            aform.save_m2m()
            signals.celery_update_index.send(sender=None,object=restaurant)
            #------- sending response
            messages.success(request, str(RESTAURANT_MSG['RUS']))
            return HttpResponseRedirect(reverse('staff_restaurant_home')) #... it willl be a GET request
        else:
            print form.errors

    else:
        print "GET..."
        data={}
        data['restaurant']=restaurant
        data['form'] = form
        data['wform']=wform
        data['aform']=aform
        data['address']=address
        return render_to_response('restaurants/staff/update_restaurant.html', data, context_instance=RequestContext(request))
      






#========================================= Menu
@staff_member_required    
def restaurant_menu(request, id):
    data={}
    data['restaurant']=restaurant= Restaurants.objects.prefetch_related('restaurant_menus').get(id=id)
    return render_to_response('restaurants/staff/menu.html',data, context_instance=RequestContext(request))


@staff_member_required     
def restaurant_add_menu(request, id):
    data={}
    try:restaurant = Restaurants.objects.get(id = id)
    except:return HttpResponseRedirect(reverse('staff_restaurant_home'))
    try:  #.....update
        menu_obj = RestaurantMenus.objects.get(id= request.REQUEST['mid'], restaurant = restaurant)
        form = RestaurantMenusForm(instance = menu_obj)
    except: 
        menu_obj = None 
        form = RestaurantMenusForm()
        
    data['restaurant'] = restaurant    
    data['menu_obj'] = menu_obj    
    
    if request.method=="POST":
        form = RestaurantMenusForm(request.POST, request.FILES, instance = menu_obj )
        if form.is_valid():
            print "form valid..." 
            menu = form.save(commit=False)
            menu.restaurant=restaurant
            menu.uploaded_by = request.user
            menu.save()
            form.save_m2m()
            messages.success(request, str(RESTAURANT_MSG['RMUS']))
            return HttpResponseRedirect(reverse('staff_restaurant_menu',args=[restaurant.id])) 
    else:
        print "GET.............."
        data['form']=form
        return render_to_response("restaurants/staff/update_menu.html", data, context_instance=RequestContext(request))



@staff_member_required
def restaurant_delete_menu(request):
    try:
        if request.user.has_perm('restaurants.add_restaurants') and request.user.has_perm('restaurants.change_restaurants'):
            menu=RestaurantMenus.objects.get(id=int(request.POST['id']))
            menu.delete()
            return HttpResponse(simplejson.dumps({'status':1,'msg':str(RESTAURANT_MSG['RMDS']),'mtype':get_msg_class_name('s')}))
        else:
            return HttpResponse(simplejson.dumps({'status':0,'msg':str(RESTAURANT_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    except:
        return HttpResponse(simplejson.dumps({'status':0,'msg':str(RESTAURANT_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

@staff_member_required
def restaurant_menu_load_html(request):
    try:
        if request.user.has_perm('restaurants.add_restaurants') and request.user.has_perm('restaurants.change_restaurants'):
            menu=RestaurantMenus.objects.get(id=int(request.POST['id']))
            html=render_to_string('restaurants/staff/load_menu.html',{'menu':menu},context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'html':html,'status':1}))
        else:
            return HttpResponse(simplejson.dumps({'status':0}))
    except:
        return HttpResponse(simplejson.dumps({'status':0}))



#========================================= image
@staff_member_required
def restaurant_images(request, id, template='restaurants/staff/image.html'):
    restaurant_obj = Restaurants.objects.prefetch_related('restaurant_images').get(id = id)
    data = {'restaurant_obj':restaurant_obj}
    return render_to_response(template, data, context_instance = RequestContext(request))



@login_required
def ajax_upload_image(request, id):
    print "up..........."
    restaurant_obj = Restaurants.objects.get(id = id)
    return upload_photos(request, RestaurantImages, restaurant_obj, 'restaurant', False,False,False) # Method written in 



@login_required
def restaurant_delete_images(request, pk):
    return delete_photos(request, RestaurantImages, pk)



@login_required
def ajax_update_photo_caption(request, pk, template='common/update-photo-caption.html'):
    from common.fileupload import update_photo_caption
    data = {}
    photo = RestaurantImages.objects.get(id=pk, uploaded_by = request.user)
    data['photo'] = photo
    data['html'] = template
    if request.method == 'POST':
        return update_photo_caption(request, photo) #calling method wriiten in common/fileupload.py
    return render_to_response(template,data, context_instance=RequestContext(request))




#========================================= Videos

@staff_member_required
def restaurant_videos(request, template = 'restaurants/staff/video.html'):
    restaurant_obj = Restaurants.objects.prefetch_related('restaurant_videos').get(id = request.GET['rid'])
    data = {'restaurant_obj':restaurant_obj}
    return render_to_response(template, data, context_instance = RequestContext(request))


@staff_member_required
def restaurant_ajax_add_videos(request, template='restaurants/staff/video-list.html'):
    data={}
    try:
        restaurant_obj = Restaurants.objects.get(id = request.GET['rid'])
        video = RestaurantVideos(restaurant = restaurant_obj)
        is_vimeo = request.GET.get('is_vimeo','false')
        title = request.GET['title']
        if not title:title = restaurant_obj.title
        video.title = title
        video.video_url = request.GET['vid']
        video.created_by = request.user
        if is_vimeo != 'false':
            video.is_vimeo = True
            video.vimeo_image = request.GET['image']
        video.save()
        data['status'] = True
        restaurant_obj = Restaurants.objects.prefetch_related('restaurant_videos').get(id = request.GET['rid'])
        html=render_to_string(template,{'restaurant_obj':restaurant_obj})
        data['html'] = html
    except:
        data['status'] = False
    return HttpResponse(simplejson.dumps(data)) 



@staff_member_required    
def restaurant_ajax_delete_videos(request):
    data = {}
    try:
        restaurant_obj = Restaurants.objects.get(id = request.GET['rid'])
        video = RestaurantVideos.objects.get(id=request.GET['vid'],restaurant = restaurant_obj)
        video.delete()
        data['status'] = True
        data['total_videos'] = RestaurantVideos.objects.filter(restaurant = restaurant_obj).count()
    except:
        data['status'] = False
    return HttpResponse(simplejson.dumps(data)) 










#......................................................................


@staff_member_required
def ajax_list_restaurant(request, template='restaurants/staff/ajax_listing.html'):
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


def filter_search(request):
    print "filter.........."
    data={}
    key={}
    args = q=()
    msg = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    print "mmmmmmm...........",listing_type
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-created_on')
    
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))
    
    if status!='all' and status!='':
        key['status'] = status
    if listing_type !='all':
        key['featured_sponsored'] = listing_type    
    if created!='all':
        if created =='CSM':
            key['created_by'] = request.user
        else:
            args = (~Q(created_by = request.user))
            
            
            
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
                    restaurants = Restaurants.objects.filter(~Q(status='D'),q,**key).select_related('categories','created_by').order_by(sort)
                else:
                    restaurants = Restaurants.objects.filter(~Q(status='D'),q,**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :
                restaurants = Restaurants.objects.filter(~Q(status='D'),**key).select_related('categories','created_by').order_by(sort)
            else:
                restaurants = Restaurants.objects.filter(~Q(status='D'),**key).select_related('categories','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :
            restaurants = Restaurants.objects.filter(~Q(status='D'),**key).select_related('categories','created_by').order_by(sort)
        else:
            restaurants = Restaurants.objects.filter(~Q(status='D'),args,**key).select_related('categories','created_by').order_by(sort)
    #....... search done
    
            
    restaurants = restaurants.distinct()
    data = ds_pagination(restaurants,page,'restaurants',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    #data['restaurant']=restaurants
    return data
    
    
    
    
    
    
    
@staff_member_required
def ajax_restaurant_action(request, template='restaurants/staff/ajax_delete_listing.html'):
    print "restaurant action.........."
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    restaurant = Restaurants.objects.filter(id__in=id)
    status=0

    #print "ids...", id
    #print "all_ids", all_ids
    if action=='DEL':
        if request.user.has_perm('restaurants.delete_restaurants'):
            signals.celery_delete_indexs.send(sender=None,objects=restaurant)
            restaurant.delete()
            status=1
            msg=str(RESTAURANT_MSG['RDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('restaurants.publish_restaurants'):
            restaurant.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=restaurant)
            if action=='P':
                try:
                    for rest in restaurant:
                        mail_publish_restaurant(rest)
                except:
                    pass
            status=1
            msg=str(RESTAURANT_MSG['RSCS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    
    
    
    
    
    data=filter_search(request)
    new_id=[]#...... all ids in DB 
    
    for cs in data['restaurants']:
        new_id.append(int(cs.id)) #...... all ids in DB 
    
    #print "new_id[]...", new_id
       
    for ai in id:
        all_ids.remove(ai)
        
    #print "all_ids", all_ids

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
    #print "new_id", new_id
    data['new_id']=new_id
  
    
    send_data={}
    send_data['html']=render_to_string(template, data, context_instance=RequestContext(request))
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
    
    
@staff_member_required
@permission_required('restaurants.change_restaurants',raise_exception=True)      
def seo_restaurant(request, id, template='restaurants/staff/update_seo.html'):
    print "seo......rest"
    restaurant = Restaurants.objects.get(id = id)
    print restaurant.seo_title
    form=RestaurantSEOForm(instance=restaurant)
    if request.POST:
        form=RestaurantSEOForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(RESTAURANT_MSG['ASUS'])}))
        else:
            data={'form':form,'restaurant':restaurant}
            return error_response(request,data,template, RESTAURANT_MSG)
    data={'form':form,'restaurant':restaurant}
    return render_to_response(template, data, context_instance=RequestContext(request))
    
    
    
    
    
@staff_member_required
@permission_required('restaurants.promote_restaurants',raise_exception=True)    
def restaurant_listing_type(request,template='restaurants/staff/ajax_listing_type.html'):
    print "restaurant_listing_type......"
    data={}
    data['restaurant'] = restaurant= Restaurants.objects.get(id=int(request.REQUEST['id']))
    if request.method=="POST":
            #................ saving pricing info
            listing_type = RestaurantPrice.objects.get(id=int(request.POST['listingtype']))
            if listing_type.level=='level2':
                restaurant.featured_sponsored="F"
                pass
            elif listing_type.level=='level1':
                restaurant.featured_sponsored="S"
            else:
                restaurant.featured_sponsored="B"
            restaurant.payment=listing_type
            
            try:
                dfmt = '%d/%m/%Y'
                restaurant.start_date=datetime.datetime.strptime(request.POST['start_date'], dfmt)
                restaurant.end_date=datetime.datetime.strptime(request.POST['end_date'], dfmt)
                print "...........dddddddddddd", restaurant.start_date
                #business.lstart_date=request.POST['start_date']
                #business.lend_date=request.POST['end_date']
            except:
                restaurant.start_date = request.POST['start_date']
                restaurant.end_date =   request.POST['end_date']
                
            if listing_type!="level0":
                restaurant.is_paid=True
                restaurant.payment_type=request.POST['period']
                save_to_paymentorder(request, restaurant, listing_type.level_label, restaurant.start_date, restaurant.end_date)
            else:
                restaurant.is_paid=False
           
            restaurant.save()
            
            return HttpResponse(simplejson.dumps({'status':1,'listingtype':restaurant.featured_sponsored,'id':restaurant.id,'mtype':get_msg_class_name('s'),'msg':str(RESTAURANT_MSG['RLUS'])}))
                
                
                
    else:
        data['restaurant_price_objects']=RestaurantPrice.objects.filter(level_visibility=True).order_by('id')   
        return render_to_response(template, data, context_instance=RequestContext(request))
    


@staff_member_required
def ajax_restaurant_state(request):
    print "restaurant state.........."
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}

    if status == 'all':
        restaurant_state = Restaurants.objects.values('status').annotate(s_count=Count('status')).exclude(status='D')
    else:
        restaurant_state = Restaurants.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status')).exclude(status='D')

    for st in restaurant_state:
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



@staff_member_required
@permission_required('restaurants.publish_restaurants',raise_exception=True)
def change_status_restaurant(request):
    print "change_status_restaurant......"
    try:
        restaurant = Restaurants.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        restaurant.status = status
        if status=='P':
            try:mail_publish_restaurant(restaurant)
            except:pass
        restaurant.save()
        signals.celery_update_index.send(sender=None,object=restaurant)
        html ='<span title="'+restaurant.get_status().title()+'" name="'+restaurant.status+'" id="id_estatus_'+str(restaurant.id)+'" class="inline-block status-idty icon-'+restaurant.get_status()+'"></span> '
        return HttpResponse(html)
    except:return HttpResponse('0')











    