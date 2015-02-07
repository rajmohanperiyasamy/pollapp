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

#Module Files(models,forms etc...)
from flowers.models import FlowerApiSettings,Category,Flowers

ITEMS_PER_PAGE = 21

def flowers_home(request,catslug='all',template='default/flowers/flowers-home.html'):
    ''' listing all flowers '''
    data={}
    key={}
    page = int(request.REQUEST.get('page',1))
    sort = request.REQUEST.get('sort','price')
    
    try:
        price_range = request.REQUEST['price-range']
        if price_range == 'below40':key['price__range']=(0,40)
        elif price_range == '40-60':key['price__range']=(40,60)
        elif price_range == '60-80':key['price__range']=(60,80)  
        elif price_range == '80-100':key['price__range']=(80,100)        
        else:key['price__gt']=100       
    except:price_range=False
            
    try:
        category = Category.objects.get(slug=catslug)
        flowers = Flowers.objects.filter(categories=category,is_active=True,**key).prefetch_related('categories').order_by(sort)
        url = category.get_absolute_url()
    except:
        category = False
        flowers = Flowers.objects.filter(is_active=True,**key).prefetch_related('categories').order_by(sort)
        url = reverse('flowers_flowers_home')
        
    data = ds_pagination(flowers,page,'flowers',ITEMS_PER_PAGE)
    data['url'] = url
    data['seo'] = ModuleNames.get_module_seo(name='flowers')
    data['price_range'] = price_range
    data['sort'] = sort
    data['selected_category'] = category
    data['view_type'] = request.GET.get('view','grid')
    return render_to_response(template,data,context_instance=RequestContext(request))  
    
def flowers_search(request,template='default/flowers/flowers-home.html'):
    ''' flowers searching methods '''
    key={}
    key_or=False
    page = int(request.REQUEST.get('page',1))
    key['is_active'] = True
    sort = request.REQUEST.get('sort','price')
    
    try:
        price_range = request.REQUEST['price-range']
        if price_range == 'below40':key['price__range']=(0,40)
        elif price_range == '40-60':key['price__range']=(40,60)
        elif price_range == '60-80':key['price__range']=(60,80)  
        elif price_range == '80-100':key['price__range']=(80,100)        
        else:key['price__gt']=100       
    except:price_range=False
        
    try:
        q=request.REQUEST.get('q','')
        key_or = (Q(name__icontains=q) | Q(categories__name__icontains=q) |Q(description__icontains=q))
    except:pass  
    try:
        category = Category.objects.get(id=request.REQUEST['category'])
        key['categories']=category
    except:
        category='all'
        pass
    
    if key_or :
         flowers = Flowers.objects.filter(key_or,**key).prefetch_related('categories').distinct().order_by(sort)
    else:flowers = Flowers.objects.filter(**key).prefetch_related('categories').distinct().order_by(sort) 
    
    data = ds_pagination(flowers,page,'flowers',ITEMS_PER_PAGE)
    data['url'] = reverse('flowers_flowers_search')
    data['seo'] = ModuleNames.get_module_seo(name='flowers')
    data['price_range'] = price_range
    data['search'] = True
    data['q'] = q
    data['category'] = category
    data['sort']=sort
    data['view_type'] = request.GET.get('view','grid')
    return render_to_response(template,data,context_instance=RequestContext(request))  
    
def flower_details(request,slug,template='default/flowers/flowers-detail.html'):
    ''' flowers detail '''
    data={}
    try:flower = Flowers.objects.prefetch_related('categories').get(slug=slug,is_active=True)
    except:return HttpResponseRedirect(reverse('flowers_flowers_home'))  
    data['flower'] = flower
    data['seo'] = ModuleNames.get_module_seo(name='flowers')
    data['scaptcha'] = captcha.getCaptcha()
    data['allcategories'] = Category.objects.filter(parent__isnull=False).order_by('name')
    return render_to_response(template,data,context_instance=RequestContext(request))

def flowers_auto_suggest(request):
    ''' autosuggest flower top search'''
    try:
        q = request.POST['query']
        data = Flowers.objects.filter(is_active=True,name__icontains=q).distinct()[:10]
    except:data = False
    child_dict = []
    if data:
        for item in data :
            buf={'id':item.id,'name':item.name}
            child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), content_type="application/json")  
