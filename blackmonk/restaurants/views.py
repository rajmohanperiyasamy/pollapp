#Python Libs 
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

#Django Libs 
from django.db.models import Q, Count
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings as my_settings

#Application Libs and Common Methods
from common.utils import ds_pagination, get_global_settings
from common.models import ModuleNames
from usermgmt.models import Favorite
from usermgmt.favoriteviews import add_remove_fav,get_fav

#Module Files(models,forms etc...)
from restaurants.models import RestaurantCategories, Restaurants, Cuisines, RestaurantImages, RestaurantFeatures, RestaurantAddress, RestaurantMenus
    
ITEMS_PER_PAGE = 15
GET_PRICE_RANGE_FORMAT = {'25':'$', '50':'$$', '75':'$$$','100':'$$$$'}

def __get_price_range(price):
    try:
        if price == '25':org_price = (1,25)
        elif price == '50':org_price = (26,50)
        elif price == '75':org_price = (51,75)
        else:org_price = (76,100)
    except:org_price = price        
    return org_price

def restaurants_home(request, template='default/restaurants/home.html'):
    ''' listing all hotels '''
    data={}
    data['popular_cuisines'] =  Cuisines.objects.annotate(rest_count = Count('restaurant_cuisines')).prefetch_related('restaurant_cuisines').order_by('-rest_count')[:4]
    data['latest_photos'] = RestaurantImages.objects.only('title','photo','restaurant').filter(restaurant__status='P').order_by('-restaurant').distinct()[:6]
    return render_to_response(template,data,context_instance=RequestContext(request))  

def restaurants_listing(request, cuisineslug='all', template='default/restaurants/restaurants-listing.html'):
    try:cuisine = Cuisines.objects.get(slug = cuisineslug)
    except:cuisine = False    
    page = int(request.GET.get('page',1))
    if cuisine:
        restaurants = Restaurants.objects.only('name','slug','ratings','price_range','logo','cuisines').filter(cuisines = cuisine, status='P').prefetch_related('restaurant_address','cuisines').select_related('logo').order_by('-id')
    data = ds_pagination(restaurants,page,'restaurants',ITEMS_PER_PAGE)
    data['selected_cuisine'] = cuisine
    data['sort'] = '-id'
    data['view_type'] = request.GET.get('view','list')
    return render_to_response(template,data,context_instance=RequestContext(request))  

def __filter_restaurants(request):
    
    key={}
    key_or = False
    ordervals=[]
    key['status'] = 'P'
    sort = request.GET.get('sort','-id')
    page = int(request.GET.get('page',1))
    ordervals.append(sort)
        
    try:cusines = request.GET['cuisines'].split(',')
    except:cusines = request.GET['cuisines']
    try:categories = request.GET['categories'].split(',')
    except:categories = request.GET['categories']
    
    try:features = request.GET['features'].split(',')
    except:features = request.GET['features']
    try:prices = request.GET['prices'].split(',')
    except:prices = request.GET['prices']
    
    if cusines != [u'0']:key['cuisines__id__in'] = cusines
    if categories != [u'0']:key['categories__id__in'] = categories 
    if features != [u'0']:key['features__id__in'] = features
    if prices != [u'0']:
        key['price_range__in'] = prices
        ordervals.append('price_range')
    
    search = request.GET.get('search',False)
    q = request.REQUEST.get('q','').strip()
    location = request.REQUEST.get('location','').strip()
    
    if search:
        try:key_or = (Q(name__icontains=q) | Q(categories__name__icontains=q) | Q(description__icontains=q) | Q(cuisines__name__icontains=q) | Q(features__name__icontains=q))
        except:pass  
        try:
            rids=[0]
            if location:
                try:loc = location.split('-')[0].strip()
                except:loc = location
                address = RestaurantAddress.objects.filter(Q(address1__icontains=loc)|Q(address2__icontains=loc)|Q(pin__icontains=loc)|Q(city__icontains=loc),restaurant__status='P')
                for add in address:rids.append(add.restaurant.id)
                key['id__in'] = rids
        except:pass
        
    try:
        if key_or:restaurants = Restaurants.objects.only('name','slug','ratings','price_range','logo','cuisines').filter(key_or,**key).prefetch_related('restaurant_address','cuisines').select_related('logo').distinct()
        else:restaurants = Restaurants.objects.only('name','slug','ratings','price_range','logo','cuisines').filter(**key).prefetch_related('restaurant_address','cuisines').select_related('logo').distinct()
    except:restaurants = Restaurants.objects.only('name','slug','ratings','price_range','logo','cuisines').filter(**key).prefetch_related('restaurant_address','cuisines').select_related('logo').distinct()      
    
    restaurants = restaurants.order_by(*ordervals)
    data = ds_pagination(restaurants,page,'restaurants',ITEMS_PER_PAGE)
    data['sort'] = sort
    try:data['selected_cuisine'] = Cuisines.objects.get(id = request.GET['sel_cuisine'])
    except:data['selected_cuisine'] = False
    data['search'] = search
    data['location'] = location
    data['kw'] = q
    data['view_type'] = request.GET.get('view','list')
    return data    

def list_restaurants_by_types(request, template='default/restaurants/restaurants-listing.html'):
    key={}
    sort = request.GET.get('sort','-id')
    page = int(request.GET.get('page',1))
    key['status'] = 'P'
    key_or = False
    prices = request.GET.get('price_range',False)
    search = request.GET.get('search',False)
    q=request.REQUEST.get('q','').strip()
    location = request.REQUEST.get('location','').strip()
    
    if search:
        try:key_or = (Q(name__icontains=q) | Q(categories__name__icontains=q) | Q(description__icontains=q) | Q(cuisines__name__icontains=q) | Q(features__name__icontains=q))
        except:pass  
        try:
            rids=[0]
            if location:
                try:loc = location.split('-')[0].strip()
                except:loc = location
                address = RestaurantAddress.objects.filter(Q(address1__icontains=loc)|Q(address2__icontains=loc)|Q(pin__icontains=loc)|Q(city__icontains=loc),restaurant__status='P')
                for add in address:rids.append(add.restaurant.id)
                key['id__in'] = rids
        except:pass
    
    try:category = RestaurantCategories.objects.get(id = request.GET['food-type'])
    except:category = False 
    try:feature = RestaurantFeatures.objects.get(id = request.GET['feature'])
    except:feature = False                                              
    
    if prices:key['price_range__range'] = __get_price_range(prices)
    if category:key['categories'] = category 
    if feature:key['features'] = feature
    
    if key_or:restaurants = Restaurants.objects.only('name','slug','ratings','price_range','logo','cuisines').filter(key_or,**key).prefetch_related('restaurant_address','cuisines').select_related('logo').order_by('-id').distinct()
    else:restaurants = Restaurants.objects.only('name','slug','ratings','price_range','logo','cuisines').filter(**key).prefetch_related('restaurant_address','cuisines').select_related('logo').order_by('-id').distinct()
    
    data = ds_pagination(restaurants,page,'restaurants',ITEMS_PER_PAGE)
    data['sort'] = sort
    data['sel_prices'] = int(prices)
    data['sel_category'] = category
    data['sel_feature'] = feature
    data['search'] = search
    data['location'] = location
    data['kw'] = q
    data['view_type'] = request.GET.get('view','list')
    return render_to_response(template,data,context_instance=RequestContext(request))  

def ajajx_restaurants_listing(request, template='default/restaurants/part-restaurants-list.html'):   
    send_data = {}
    try:
        data=__filter_restaurants(request)
        send_data['html'] = render_to_string(template,data,context_instance=RequestContext(request))
        send_data['status'] = True
        if data['count']!=0:
            send_data['pagntn_ranges_txt'] = _('Showing ')+str(data['from_range'])+'-'+str(data['to_range'])+_(' of ')+str(data['count'])
        else:send_data['pagntn_ranges_txt'] = False
    except:send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def restaurants_get_selected_values(request, template='default/restaurants/update-restaurant-selected-values.html'):
    data = {}
    send_data = {}
    send_values = []
    '''try:cusines = request.GET['cuisines'].split(',')
    except:cusines = request.GET['cuisines']'''
    
    try:categories = request.GET['categories'].split(',')
    except:categories = request.GET['categories']
    try:prices = request.GET['prices'].split(',')
    except:prices = request.GET['prices']
    try:features = request.GET['features'].split(',')
    except:features = request.GET['features']
    
    '''try:
        cusines_list = Cuisines.objects.filter(id__in=cusines)
        for cs in cusines_list:
            send_values.append({'id':cs.id, 'name':cs.name, 'type':'cuisns'})
    except:pass'''
            
    try:
        categories_list = RestaurantCategories.objects.filter(id__in = categories)
        for cat in categories_list:
            send_values.append({'id':cat.id, 'name':cat.name, 'type':'catgrs'})
    except:pass
    try:
        if prices != [u'0']:
            for price in prices:
                if price !='0':send_values.append({'id':price, 'name':GET_PRICE_RANGE_FORMAT[price], 'type':'price'})
            
    except:pass
    try:    
        features_list = RestaurantFeatures.objects.filter(id__in = features)
        for fl in features_list:
            send_values.append({'id':fl.id, 'name':fl.name, 'type':'ftrs'})    
    except:pass    
    
    sorted_list = sorted(send_values, key=lambda k: k['name'])
    data['sorted_list'] = sorted_list
    
    if sorted_list:list_contents = True
    else:list_contents = False
    send_data['html'] = render_to_string(template,data,context_instance=RequestContext(request))
    send_data['status'] = True
    send_data['list_contents'] = list_contents
    return HttpResponse(simplejson.dumps(send_data))

def restaurant_details(request, slug, template='default/restaurants/restaurant-details.html'):
    try:restaurant = Restaurants.objects.prefetch_related('restaurant_address','cuisines','restaurant_images','categories',
                                                          'meal_types','paymentoptions','restaurant_menus','categories','features','tags').select_related('logo','workinghours').get(slug=slug,status='P')
    except:return HttpResponseRedirect(reverse('restaurants_restaurants_home'))                                                      
    view = request.GET.get('view','home')
    try:
        restaurant.views+=1
        restaurant.save()
    except:pass
    data = {'restaurant':restaurant,'view':view}
    data['today'] = date.today()
    return render_to_response(template,data,context_instance=RequestContext(request))

def retrieve_menus_by_type(request, template='default/restaurants/menu-list.html'):
    send_data = {}
    try:
        menu_list = RestaurantMenus.objects.filter(categories__id = request.GET['mid'], restaurant__id = request.GET['rid'])
        data = {'menu_list':menu_list}
        send_data['html'] = render_to_string(template,data,context_instance=RequestContext(request))
        send_data['status'] = True
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))
    
def auto_suggest_restaurants(request):
    try:
        q=request.POST['query']
        q_key=(Q(name__icontains=q)|Q(description__icontains=q)|Q(categories__name__icontains=q))
        data = Restaurants.objects.filter(q_key,status='P').distinct()[:10]
    except:
        data = False
    child_dict = []
    if data:
        for restaurant in data :
            buf={'id':restaurant.id,'name':restaurant.name}
            child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), content_type="application/json")

def auto_suggest_restaurant_locations(request):
    try:
        q=request.POST['query']
        q_key=(Q(address1__icontains=q)|Q(address2__icontains=q)|Q(pin__icontains=q)|Q(city__icontains=q))
        data = RestaurantAddress.objects.filter(q_key,restaurant__status='P').distinct()[:10]
    except:data = RestaurantAddress.objects.filter(restaurant__status='P').distinct()[:10]
    child_dict = []
    for adr in data :
        name = adr.address1
        if adr.city:name+=' - '+adr.city
        buf={'id':adr.id, 'name':name}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), content_type="application/json")    
