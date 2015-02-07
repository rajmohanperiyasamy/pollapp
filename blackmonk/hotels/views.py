# Python Libs 
from datetime import date
import math

# Django Libs 
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect

#Application Libs and Common Methods
from common import captcha
from common.models import ModuleNames
from common.utils import ds_pagination
from django.conf import settings as my_settings
from common.utils import get_global_settings
#Module Files(models,forms etc...)
from hotels.models import ApiSettings,Category,Amenities,HotelDetails,Hotels,HotelImages,RoomAmenities,HotelRoomDetails

ITEMS_PER_PAGE=12

def hotels_home(request,catslug='all',template='default/hotels/home.html'):
    ''' listing all hotels '''
    data={}
    sort = request.REQUEST.get('sort','rating')
    if sort=='lh':order='lowrate'
    elif sort =='hl':order='-lowrate'
    else:order='-hotel_rating'
    page = int(request.REQUEST.get('page',1))
    try:
        category = Category.objects.get(slug=catslug)
        hotels = Hotels.objects.filter(category=category,is_active=True).prefetch_related('category','amenities','details','hotel_images').order_by(order)
        url = category.get_absolute_url()
    except:
        hotels = Hotels.objects.filter(is_active=True).prefetch_related('category','amenities','details','hotel_images').order_by(order)
        url = reverse('hotels_home')
    try:
        expedia_api = ApiSettings.objects.all()[:1][0]
    except:
        expedia_api = None
    data = ds_pagination(hotels,page,'hotels',ITEMS_PER_PAGE)
    data['categories'] = categories = Category.objects.all().order_by('name')
    data['remndr']=int(math.ceil(categories.count()*1.0/2.0))
    data['url'] = url
    data['seo'] = ModuleNames.get_module_seo(name='hotels')
    data['sort']=sort
    data['expedia_api']=expedia_api
    return render_to_response(template,data,context_instance=RequestContext(request))  
    
def hotel_details(request,slug,template='default/hotels/hotel-details.html'):
    ''' hotel details page '''
    data={}
    try:hotel = Hotels.objects.prefetch_related('category','amenities','details','hotel_images','hotel_rooms').get(slug=slug)
    except:return HttpResponseRedirect(reverse('hotels_home'))  
    data['hotel'] = hotel
    data['seo'] = ModuleNames.get_module_seo(name='hotels')
    data['scaptcha'] = captcha.getCaptcha()
    try:data['hotel_api_settings'] = ApiSettings.objects.all()[:1][0]
    except:data['hotel_api_settings']=False
    return render_to_response(template,data,context_instance=RequestContext(request))
    
def ajax_tell_a_friend(request):
    ''' ajax method for sending email (particular hotel details) to friend '''
    scaptcha={}
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    if request.method == 'POST':
        hotel = Hotels.objects.get(id=request.POST['content_id'])
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        to_email = request.POST['to_email']
        msg = request.POST['msg']
        subject = from_name+' sent you hotel details of "'+hotel.name+'" -'+global_settings.domain
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['hotel'] = hotel
        email_message = render_to_string("default/hotels/mail_tell_a_friend.html",tell_a_friend_data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_email])
        email.content_subtype = "html"
        email.send()
        scaptcha['success'] = 1
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)
    scaptcha['success'] = 0
    data  = simplejson.dumps(scaptcha)
    return HttpResponse(data)

def hotel_search(request,template='default/hotels/home.html'):
    ''' hotels search method  '''
    sort = request.REQUEST.get('sort','rating')
    if sort=='lh':order='lowrate'
    elif sort =='hl':order='-lowrate'
    else:order='-hotel_rating'
    key={}
    key_or=False
    page = int(request.REQUEST.get('page',1))
    key['is_active'] = True

    try:
        q=request.REQUEST.get('q','')
        key_or = (Q(name__icontains=q) | Q(category__name__icontains=q) | Q(amenities__name__icontains=q) | Q(short_description__icontains=q) | Q(details__property_information__icontains=q) | Q(details__property_description__icontains=q))
    except:pass  
    try:
        location = request.REQUEST.get('location','').strip()
        if location:
            key_or = (Q(address__icontains=location) | Q(city__icontains=location) | Q(postal_code__icontains=location) | Q(state_province_code__icontains=location) | Q(country_code__icontains=location))
    except:pass
    
    if q!='' or location!='' :
         hotels = Hotels.objects.filter(key_or,**key).prefetch_related('category','amenities','details','hotel_images').distinct().order_by(order)
    else:hotels = Hotels.objects.filter(**key).prefetch_related('category','amenities','details','hotel_images').distinct().order_by(order) 
    
    try:
        if hotels.count()==1:
            for h in hotels:
                url = h.get_absolute_url()
                return HttpResponseRedirect(url)
        else:pass            
    except:pass    
    
    data = ds_pagination(hotels,page,'hotels',ITEMS_PER_PAGE)
    data['categories'] = categories = Category.objects.all().order_by('name')
    data['remndr']=int(math.ceil(categories.count()*1.0/2.0))
    data['url'] = reverse('hotels_hotel_search')
    data['seo'] = ModuleNames.get_module_seo(name='hotels')
    data['search'] = True
    data['location'] = location
    data['q'] = q
    data['sort'] = sort
    return render_to_response(template,data,context_instance=RequestContext(request))  
    
def hotel_auto_suggest(request):
    ''' auto suggest hotel search '''
    try:
        name=request.GET['q']
        hotels = Hotels.objects.filter(is_active=True,name__icontains=name).order_by('name')[:10]
    except:
        hotels = Hotels.objects.filter(is_active=True).order_by('name')[:10]
    results = []
    for hotel in hotels:
        results.append(hotel.name)
    return HttpResponse('\n'.join(results), mimetype='text/plain')
