import math
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q, Count
from django.utils import simplejson
from django.contrib.gis.geoip import GeoIP
from googlemaps import GoogleMaps

from common.models import ModuleNames
from common.utils import ds_pagination, ds_sortby_listingtype
from django.conf import settings as my_settings

from business.models import BusinessCategory,Business,Address,BizAttributes,BusinessCoupons,BusinessProducts,Attributes,AttributeValues,BusinessClaimSettings
from business.forms import ContactDetailsForm#,CaptchaForms
from usermgmt.favoriteviews import add_remove_fav,get_fav

NUMBER_DISPLAYED = 10
orderval = ['id','name','most_viewed','ratings','-id','-name','-most_viewed','-ratings']
SORT_VALUES = {'bm':'-id', 'ratings':'-ratings'}
geoip_obj = GeoIP()

def get_distance_sorted(location,business):
    try:
        gmaps = GoogleMaps()
        long, long = gmaps.address_to_latlng(location)
        range=100
        use_miles=False
        if use_miles:distance_unit = 3959
        else:distance_unit = 6371
            
        distance_query="""SELECT (%f * acos( cos( radians(%f) ) * cos( radians( lat ) ) *
            cos( radians( lon ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( lat ) ) ) ) FROM business_address WHERE  business_address.business_id=business_business.id
            """ % (distance_unit,lant, long, lant)
            
        business=Business.objects.extra(
            select={'distances':distance_query},
            where=["id=(SELECT business_id FROM business_address WHERE business_address.business_id=business_business.id AND (%d * acos( cos( radians(%f) ) * cos( radians( lat ) ) * cos( radians( lon ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( lat ) ) ) )< %d)"%(distance_unit,lant, long, lant,range)]
        ).order_by("distances")

        return business 
    except:return business

def auto_suggest_geolocation(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for: ip = x_forwarded_for.split(',')[0]
        else:ip = request.META.get('REMOTE_ADDR')
        return HttpResponse(geoip_obj.city(ip)['city'])
    except:return HttpResponse('')
    
def business_home(request):
    try:search = request.GET['search']
    except:search = False
    buscategory = BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('name')
    if search:
        data = business_filter(request,False,search)
        data['seo'] = ModuleNames.get_module_seo(name='business')
        data['categories'] = buscategory
        return render_to_response('default/business/businesslist.html',data, context_instance=RequestContext(request))
    else:
        data = {'buscategory': buscategory}
        data['seo'] = ModuleNames.get_module_seo(name='business')
        data['popular_categories'] = BusinessCategory.objects.annotate(num_business=Count('allcategories')).filter(parent_cat__isnull=False,num_business__gt=3)[:20]
        return render_to_response('default/business/categorylist.html',data, context_instance=RequestContext(request))

def business_list(request,catslug=False):
    if catslug:
        data = business_filter(request,catslug,False)
        if not data:
            return HttpResponseRedirect(reverse('business_home'))
        #if data['count']==1:
        #    for b in data['businesslist']:return HttpResponseRedirect(b.get_absolute_url())
        data['url'] = reverse('business_listing',args=[catslug])
        if data['at_id']:
            data['url']=data['url']+'?at_id='+data['at_id']
        try:
            category_attr= data['selectedcat']
            if category_attr.parent_cat:
                #data['attributes']= Attributes.objects.filter(Q(type='S')|Q(type='K')|Q(type='R'),(Q(category = category_attr)|Q(category = category_attr.parent_cat))).prefetch_related('attributekey','attributekey__bizattributesvalues__business__categories').order_by('-name')
                data['attributes'] = AttributeValues.objects.filter(Q(attribute_key__category = category_attr)|Q(attribute_key__category = category_attr.parent_cat)).order_by('-id')
            else:
                data['attributes'] = AttributeValues.objects.filter(attribute_key__category = category_attr).order_by('-id')
                #data['attributes']= Attributes.objects.filter(Q(type='S')|Q(type='K')|Q(type='R'),category = category_attr).prefetch_related('attributekey','attributekey__bizattributesvalues__business').order_by('-name')
        except:pass
        return render_to_response('default/business/businesslist.html',data, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('business_home'))

def business_filter(request,catslug,search):
    key={}
    q=location=''
    q_text=()
    key['status'] = 'P'
    view_type = request.GET.get('view','list')
    sort = request.REQUEST.get('sort','bm')
    order = SORT_VALUES[sort]
    if search:
        try:
            q = request.GET['q']
            q_text=(Q(name__icontains=q)|Q(description__icontains=q)|Q(categories__name__icontains=q)|Q(categories__parent_cat__name__icontains=q)|Q(tags__tag__icontains=q))
        except:pass
        try:
            bids = [0]
            location = request.GET['location'].strip()
            if location:
                key['address__id__in'] = Address.objects.filter(Q(address1__icontains=location)|Q(address2__icontains=location)|Q(zip__icontains=location)|Q(city__icontains=location),business__status='P').values_list("id", flat=True)
        except:pass
        
    if catslug:
        try:selectedcat = BusinessCategory.objects.get(slug=catslug)
        except:return False
        
        if selectedcat.parent_cat:
            parent = False
            subcat = BusinessCategory.objects.filter(slug=catslug)
            subcategories = BusinessCategory.objects.filter(parent_cat=selectedcat.parent_cat)
        else:
            parent = True
            subcat = BusinessCategory.objects.filter(parent_cat=selectedcat)
            subcategories = subcat
        key['categories__in']=subcat
        
        try:
            at_id=request.GET['at_id']
            ba = BizAttributes.objects.filter(value__id=at_id,business__status='P')
            array_ba=[]
            for b in ba:array_ba.append(b.business.id)
            key['id__in']=array_ba
        except:at_id=False
    businessall = ds_sortby_listingtype(Business)
    if q_text:businessall = businessall.filter(q_text,**key).prefetch_related('logo','categories','album').distinct()#.order_by('-featured_sponsored')
    else:businessall = businessall.filter(**key).prefetch_related('logo','categories','album').distinct()#.order_by('-featured_sponsored')
    
    #if search and location:businessall = get_distance_sorted(location,businessall) 
    
    if catslug:
        ''' featured business start '''
        fkey = {}
        fkey['status']='P'
        if selectedcat.parent_cat:fkey['categories__parent_cat'] = selectedcat.parent_cat
        else:fkey['categories__parent_cat'] = selectedcat
        fkey['featured_sponsored']='F'
        fkey['lend_date__gte']=date.today()
        featuredbusiness = set(Business.objects.filter(**fkey).prefetch_related('logo','categories','album').order_by('?')[:2])
        if len(featuredbusiness) == businessall.count():featuredbusiness=False
        else:businessall = businessall.exclude(id__in=[fb.id for fb in featuredbusiness])
        ''' featured business end '''
         
    try:page = int(request.GET['page'])
    except:page = 1
    
    businessall = businessall.order_by(order)
    
    data = ds_pagination(businessall,page,'businesslist',NUMBER_DISPLAYED)
    
    if catslug:
        data['selectedcat']= selectedcat
        data['categories']= subcategories
        data['parent']= parent
        data['seo'] = selectedcat
        data['at_id']=at_id
    if search:
        data['search'] = True
        data['q'] = q
        data['location'] = location
        
    try:data['featuredbusiness'] = featuredbusiness
    except:data['featuredbusiness'] = False   
    data['view_type'] = view_type  
    data['sort'] = sort
    return data

def business_details(request,slug):
    try:business = Business.objects.prefetch_related('categories','businessfile','album','tags','paymentoptions','bizattributes','bizattributes__key','bizattributes__value','buz_product').select_related('payment','workinghours').get(slug=slug,status='P')
    except: return HttpResponseRedirect(reverse('business_home'))
    data = {'business': business}
    
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
    data['view']=view
    data['claim']=BusinessClaimSettings.get_setting()
    data['today'] = date.today()
    #data['cap_form']= ContactDetailsForm()
    #data['res_form']= CaptchaForms()
    
    #data['object_id'] = business.id
    #data['content_type'] = 'business'
    #data['suggested_item'] = business
    #data['suggested_by'] = request.user.display_name.title()
    return render_to_response('default/business/businessdetails.html',data,context_instance=RequestContext(request))

def business_count(request,id):
    try:
        business = Business.objects.get(id=id)
        business.most_viewed = business.most_viewed + 1
        business.save()
        
        for log in business.audit_log.all()[:1]:
            log.delete()
        
        return HttpResponse('1')
    except:return HttpResponse('0')

def contact_us(request):
    send_data={}
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    business = Business.objects.prefetch_related('album').get(id=int(request.POST['bid']))
    form = ContactDetailsForm(request.POST)
    if form.is_valid():
        cd = form.save(commit=False)
        cd.business = business
        cd.save()
        subject = global_settings.domain+" | "+form.cleaned_data.get('subject')
        address = business.address.all()[0]
        if address.email:
            to_emailids = [address.email]
        else:
            to_emailids = [business.created_by.email]
        data={"Name": form.cleaned_data.get('name'),"Email": form.cleaned_data.get('email'),"Phone": form.cleaned_data.get('phone'),"Subject": form.cleaned_data.get('subject'),"Comment": form.cleaned_data.get('comment')}
        email_message = render_to_string("default/business/mail_msg.html", data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL, to_emailids)
        email.content_subtype = "html"
        email.send()
        send_data['success'] = 1
        data  = simplejson.dumps(send_data)
        return HttpResponse(data)
    else:
        send_data['success'] = 0
        data  = simplejson.dumps(send_data)
        return HttpResponse(data)


def ajax_tell_a_friend(request):
    send_data={}
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    #form=CaptchaForm(request.POST)
    if request.method == 'POST':
        #if form.is_valid():
        business = Business.objects.get(id=request.POST['content_id'])
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        to_email = request.POST['to_email']
        msg = request.POST['msg']
        subject = from_name+' sent you business details of "'+business.name+'" -'+global_settings.domain
        
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['business'] = business
        email_message = render_to_string("default/business/mail_tell_a_friend.html",tell_a_friend_data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_email])
        email.content_subtype = "html"
        email.send()
        send_data['success'] = 1
        data  = simplejson.dumps(send_data)
        return HttpResponse(data)
    send_data['success'] = 0
    data  = simplejson.dumps(send_data)
    return HttpResponse(data)
    
    
def auto_suggest_business(request):
    try:
        q=request.POST['query']
        q_key=(Q(name__icontains=q)|Q(description__icontains=q)|Q(categories__name__icontains=q)|Q(categories__parent_cat__name__icontains=q)|Q(tags__tag__icontains=q))
        data = Business.objects.filter(q_key,status='P').distinct()[:10]
    except:
        data = False
    
    child_dict = []
    if data:
        for buz in data :
            buf={'id':buz.id,'name':buz.name}
            child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), content_type="application/json")

def auto_suggest_business_address(request):
    try:
        q=request.POST['query']
        q_key=(Q(address1__icontains=q)|Q(address2__icontains=q)|Q(pin__icontains=q)|Q(city__icontains=q))
        data = Address.objects.filter(q_key,business__status='P')[:10]
    except:data = Address.objects.filter(business__status='P')[:10]
    child_dict = []
    test=[]
    for adr in data :
        buf={'id':adr.id, 'name':adr.address1}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), content_type="application/json")


def business_add_to_fav(request):
    try:
        business = Business.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(business,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')  
