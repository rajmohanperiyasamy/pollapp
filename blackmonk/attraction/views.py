import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from common.models import ModuleNames
from common.utils import ds_pagination
from django.conf  import settings as my_settings

from attraction.models import AttractionTag, AttractionCategory, Attraction, AttractionVideos
from common.models import Address
from usermgmt.favoriteviews import add_remove_fav,get_fav

NUMBER_DISPLAYED = 12

def attractions_home(request, catslug='all', template='default/attraction/home.html'):
    try:
        category = AttractionCategory.objects.get(slug = catslug)
    except:
        category = False     
    
    if category:
        attractions =  Attraction.objects.filter(category = category, status = 'P').only('name','slug','album','category','venue').select_related('venue','album').prefetch_related('category').order_by('-id')   
        url = reverse('attraction_listing',args = [catslug])
        seo = category
    else:
        attractions =  Attraction.objects.filter(status = 'P').only('name','slug','album','category','venue').select_related('venue','album').prefetch_related('category').order_by('-id')   
        url = reverse('attraction_home')
        seo = ModuleNames.get_module_seo(name='attraction')
    
    page =  int(request.GET.get('page',1))    
    data = ds_pagination(attractions, page, 'attractions', NUMBER_DISPLAYED)    
    data['url'] = url
    data['category']= category
    data['seo'] = seo
    data['view_type'] = request.GET.get('view','grid')
    return render_to_response(template,data, context_instance=RequestContext(request))

def attraction_details(request, slug, template='default/attraction/attractiondetails.html'):
    try:
        attraction = Attraction.objects.prefetch_related("attraction_video").select_related('category','venue','tag').get(slug=slug)
    except:
        return HttpResponseRedirect(reverse('attraction_home'))    
    data={'attraction':attraction}
    try:
        view=request.GET['view']
        if view!='home' and view!='photos' and view!='video' and view!='comments':view='home' 
        if view=='photos' and not attraction.album.album_photos.all():view='photos'
        if view=='video' and not attraction.attraction_video.all():view='home'
        data['view']=view
    except:data['view']='home'
    data['today'] = datetime.date.today()
    return render_to_response(template, data, context_instance=RequestContext(request))

def get_nearby_items(request, template='default/attraction/near-by-items.html'):
    send_data = {}
    try:
        attraction = Attraction.objects.prefetch_related( "attraction_video").select_related('category','venue','tag').get(id = request.GET['id'])
        data = {'attraction':attraction}
        send_data['html'] = render_to_string(template, data, context_instance=RequestContext(request))
        send_data['status'] = True
    except:send_data['status'] = False    
    return HttpResponse(simplejson.dumps(send_data))

def attraction_count(reequest,id):
    try:
        attraction = Attraction.objects.get(id=id)
        attraction.view_count = attraction.view_count + 1
        attraction.save()
        return HttpResponse('1')
    except:return HttpResponse('0')

from common.fileupload import upload_photos
@login_required
def ajax_upload_photos(request):  
    if request.method=='POST':
        attraction = Attraction.objects.get(id=request.GET['id'])
        return upload_photos(request,AttractionPhotos,attraction,'attraction',True,False)
    else:return []
    
def attraction_add_to_fav(request):
    try:
        attraction = Attraction.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(attraction,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')   

def attraction_search(request):
    seo = ModuleNames.get_module_seo(name='attraction')
    kw = request.GET.get('keyword').strip()
    cat = str(request.GET.get('category'))
    key = {}
    key['status']='P'
    key_or = (Q(name__icontains=kw) | Q(description__icontains=kw))

    if cat == 'All Categories':
        attraction_list = Attraction.objects.filter(key_or,**key).order_by('-name').distinct()
    else:
        category = AttractionCategory.objects.get(name= cat)
        attraction_list = Attraction.objects.filter(key_or,category = category,**key).order_by('-name').distinct()
    
    data = {}
    try:page = int(request.GET['page'])
    except:page = 1
    data = ds_pagination(attraction_list,page,'attractions',NUMBER_DISPLAYED)
    data['keyword'] = kw
    data['search'] = True
    data['category'] = cat.replace(' ', '+') 
    data['view_type'] = 'grid'
    return render_to_response('default/attraction/home.html',data,context_instance=RequestContext(request))
       