from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.html import strip_tags
from random import sample

from attraction.forms import AttractionForm, Attraction_SeoForm
from attraction.models import AttractionTag, AttractionCategory, Attraction, \
    AttractionVideos
from common import signals
from common.fileupload import upload_photos, delete_photos, \
    upload_photos_forgallery, delete_photos
from common.getunique import getUniqueValue
from common.models import Address
from common.staff_messages import ATTRACTION_MSG, COMMON
from common.templatetags.ds_utils import get_msg_class_name
from common.utils import ds_pagination
from common.utilviews import crop_and_save_coverphoto
from gallery.models import PhotoAlbum, PhotoCategory, Photos


attraction_album_cat = PhotoCategory.objects.get_or_create(name="Attractions", slug='attractions', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
NO_OF_ITEMS_PER_PAGE=10

def add_tags(attraction,taglist):
    attraction.tag.clear()
    for tag in taglist:
        try:objtag = AttractionTag.objects.get(tag__iexact = tag)
        except:
            objtag = AttractionTag(tag=tag)
            objtag.save()
        attraction.tag.add(objtag)
    attraction.save()

def auto_suggest_tag(request):
    try:data = AttractionTag.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:data = AttractionTag.objects.all()[:10]
    main=[]
    for ve in data:
       b={'label':ve.tag,'id':str(ve.id),'label':ve.tag}
       main.append(b)
    return HttpResponse(simplejson.dumps(main))

@staff_member_required
def manage_attraction(request,template='attraction/staff/home.html'):
    attraction = Attraction.objects.filter(~Q(status='D')).select_related('category','created_by').order_by('-created_on')
    attraction_state = Attraction.objects.values('status').annotate(s_count=Count('status'))
    
    page = int(request.GET.get('page',1))
    total = 0
    STATE={'P':0,'B':0}
    for st in attraction_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(attraction,page,'attraction',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    
    data['categories'] = AttractionCategory.objects.all().order_by('name')
    data['total'] =total
    data['published'] =STATE['P']
    data['blocked'] =STATE['B']
    data['search'] =False
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def ajax_attraction_state(request,template='attraction/staff/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
   
    if status == 'all':
        attraction_state = Attraction.objects.values('status').annotate(s_count=Count('status'))
    else:
        attraction_state = Attraction.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in attraction_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
        
    data={
          'total':total,
          'published':STATE['P'],
          'blocked':STATE['B']
    }
    return HttpResponse(simplejson.dumps(data))


@staff_member_required
def ajax_list_attraction(request,template='attraction/staff/ajax_listing.html'):
    data=filter(request)
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
def ajax_attraction_action(request,template='attraction/staff/ajax_delete_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    value = request.GET['action']
    attractions = Attraction.objects.filter(id__in=id)
    status=0
    if action=='DEL':
        if request.user.has_perm('attraction.delete_attraction'):
            signals.celery_delete_indexs.send(sender=None,objects=attractions)
            for attract in attractions:
                try:attract.album.delete()
                except:pass
            attractions.delete()
            status=1
            msg=str(ATTRACTION_MSG['ADS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if action=='True' or action=='False':
            if action=='True':action=True
            else:action=False
            if request.user.has_perm('attraction.promote_attractions'):
                attractions.update(is_featured=action)
                status=1
                msg=str(ATTRACTION_MSG['AFSCS'])
                mtype=get_msg_class_name('s')
            else:
                msg=str(COMMON['DENIED'])
                mtype=get_msg_class_name('w')
        else:
            if request.user.has_perm('attraction.publish_attraction'):
                attractions.update(status=action)
                status=1
                msg=str(ATTRACTION_MSG['ASCS'])
                mtype=get_msg_class_name('s')
            else:
                msg=str(COMMON['DENIED'])
                mtype=get_msg_class_name('w')
    if action!='DEL':signals.celery_update_indexs.send(sender=None,objects=attractions)
    data=filter(request)
    new_id=[]
    
    for attraction in attractions:
        attraction.save()
        for log in attraction.audit_log.all()[:1]:
            if value =='True':log.action_type='F'
            elif value =='False':log.action_type = 'N'
            else:log.action_type = value
            log.save()
    for cs in data['attraction']:new_id.append(int(cs.id))
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
    else:send_data['pagerange']=0-0
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['status']=status
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))

   
def filter(request):
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
    
    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':key['is_featured'] = listing_type
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:args = (~Q(created_by = request.user))
    
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        
        if search_category:
            categorys = AttractionCategory.objects.get(id=search_category)
            key['category'] = categorys
        
        if search_type:
            if search_type=='title':key['name__icontains'] = search_keyword
            elif search_type=='description':key['description__icontains'] = search_keyword
            else:key['created_by__display_name__icontains'] = search_keyword
        
        if search_keyword:
            q =(Q(name__icontains=search_keyword)|Q(description__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if len(args) == 0 :attraction = Attraction.objects.filter(~Q(status='D'),q,**key).select_related('category','created_by').order_by(sort)
            else:attraction = Attraction.objects.filter(~Q(status='D'),q,**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :attraction = Attraction.objects.filter(~Q(status='D'),**key).select_related('category','created_by').order_by(sort)
            else:attraction = Attraction.objects.filter(~Q(status='D'),**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :attraction = Attraction.objects.filter(~Q(status='D'),**key).select_related('category','created_by').order_by(sort)
        else:attraction = Attraction.objects.filter(~Q(status='D'),args,**key).select_related('category','created_by').order_by(sort)
    
    data = ds_pagination(attraction,page,'attraction',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

@staff_member_required
@permission_required('attraction.publish_attraction',raise_exception=True)
def change_status_attraction(request):
    try:
        attraction=Attraction.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        attraction.status = status
        attraction.save()
        
        for log in attraction.audit_log.all()[:1]:
            log.action_type = status
            log.save()
        
        signals.celery_update_index.send(sender=None,object=attraction)
        html ='<span title="'+attraction.get_status().title()+'" name="'+attraction.status+'" id="id_estatus_'+str(attraction.id)+'" class="inline-block status-idty icon-'+attraction.get_status()+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')

"""
####################################################################################################################
#################################################     ADD    #######################################################
####################################################################################################################
"""

@staff_member_required
@permission_required('attraction.add_attraction',raise_exception=True)
def add_attraction(request):
    data={}
    form=AttractionForm()
    if request.POST:
        form=AttractionForm(request.POST)
        if form.is_valid():
            attraction=form.save(commit=False)
            attraction.slug=getUniqueValue(Attraction,slugify(attraction.name))
            attraction.created_by =  attraction.modified_by = request.user
            attraction.status = 'P'
            attraction.is_active = True
            try:attraction.venue=Address.objects.get(id=int(request.POST['venue_id']))
            except:pass
            attraction.seo_title=attraction.name
            attraction.seo_description=strip_tags(attraction.description[:400])
            
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                if attraction and attraction.album:
                    album = attraction.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = attraction_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = attraction.name
                album.slug = getUniqueValue(PhotoAlbum, slugify(attraction.slug))
                album.seo_title = attraction.name[:70],
                album.seo_description = album.summary = attraction.description[:160]
                album.save()
                
                attraction.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
            attraction.save()
            form.save_m2m()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=attraction)
            try:tags=request.POST['tags'].split(',')
            except:tags=request.POST['tags']
            add_tags(attraction,tags)
                
            """
            try:videos=AttractionVideos.objects.get(attraction=attraction)
            except:videos=AttractionVideos(attraction=attraction,title=attraction.name)
            videos.video_url=request.POST['video_url']
            videos.added_by=request.user
            try:
                is_vimeo=request.POST['is_vimeo']
                if is_vimeo:videos.is_vimeo=True
                else:videos.is_vimeo=False
            except:videos.is_vimeo=False
            videos.save()
            """
            for log in attraction.audit_log.all():
                if log.action_type=='U':
                    log.delete()
            #photo_obj=AttractionPhotos.objects.filter(id__in=request.POST.getlist('new_pic')).exclude(attraction__isnull=False).update(attraction=attraction)
            messages.success(request, str(ATTRACTION_MSG['AAS']))
            signals.celery_update_index.send(sender=None,object=attraction)
            return HttpResponseRedirect(reverse('staff_preview_attraction',args = [attraction.id]))
    data['form']=form
    return render_to_response('attraction/staff/add_attraction.html',data,context_instance=RequestContext(request))  

def display_address(request):
    data = {}
    try:
        venue = Address.objects.get(id=request.GET['venue_id'])
        data['venue'] = venue
        template='attraction/staff/ajax_address.html'
        html=render_to_string(template,data, context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({'status':1,'html':html}))
    except:
        venue = False
        data = {'status':0,'msg':str(ARTICLE_MSG['err']),'mtype':get_msg_class_name('e')}
        return HttpResponse(simplejson.dumps(data))


@staff_member_required
@permission_required('attraction.change_attraction',raise_exception=True)
def edit_attraction(request,id):
    data={}
    data['attraction']=attraction= Attraction.objects.get(id=id)
    try:data['video']=AttractionVideos.objects.get(attraction=attraction)
    except:pass
    form=AttractionForm(instance=attraction)
    if request.POST:
        if attraction:form=AttractionForm(request.POST,instance=attraction)
        else:form=AttractionForm(request.POST)
        if form.is_valid():
            attraction=form.save(commit=False)
            attraction.slug=getUniqueValue(Attraction,slugify(attraction.name),instance_pk=attraction.id)
            attraction.modified_by = request.user
            try:attraction.venue=Address.objects.get(id=int(request.POST['venue_id']))
            except:pass
            attraction.is_active = True
            
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                if attraction and attraction.album:
                    album = attraction.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = attraction_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = attraction.name
                album.slug = getUniqueValue(PhotoAlbum, slugify(attraction.slug))
                album.seo_title = attraction.name[:70],
                album.seo_description = album.summary = attraction.description[:160]
                album.save()
                
                attraction.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
            
            attraction.save()
            form.save_m2m()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=attraction)
            try:tags=request.POST['tags'].split(',')
            except:tags=request.POST['tags']
            add_tags(attraction,tags)
           
            """
            try:videos=AttractionVideos.objects.get(attraction=attraction)
            except:videos=AttractionVideos(attraction=attraction,title=attraction.name)
            videos.video_url=request.POST['video_url']
            videos.added_by=request.user
            try:
                is_vimeo=request.POST['is_vimeo']
                if is_vimeo:videos.is_vimeo=True
                else:videos.is_vimeo=False
            except:videos.is_vimeo=False
            videos.save()
            """
            signals.celery_update_index.send(sender=None,object=attraction)
            messages.success(request, str(ATTRACTION_MSG['AUS']))
            return HttpResponseRedirect(reverse('staff_manage_attraction'))
    data['form']=form
    return render_to_response('attraction/staff/edit_attraction.html',data,context_instance=RequestContext(request))  

@staff_member_required
def preview_attraction(request,id):
    data={}
    data['attraction']=attraction= Attraction.objects.get(id=id)
    try:data['videos']=AttractionVideos.objects.filter(attraction=attraction).order_by('added_on')
    except:pass
    return render_to_response('attraction/staff/preview.html',data,context_instance=RequestContext(request))  

@staff_member_required
@permission_required('attraction.change_attraction',raise_exception=True)
def seo_attraction(request,id,template='attraction/staff/update_seo.html'):
    attraction = Attraction.objects.get(id = id)
    form=Attraction_SeoForm(instance=attraction)
    if request.POST:
        form=Attraction_SeoForm(request.POST,instance=attraction)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug=getUniqueValue(AttractionCategory,slugify(attraction.slug),instance_pk=seo.id)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(ATTRACTION_MSG['ASUS'])}))
        else:
            data={'form':form,'attraction':attraction}
            return error_response(request,data,template,ATTRACTION_MSG)
    data={'form':form,'attraction':attraction}
    return render_to_response(template,data, context_instance=RequestContext(request))


# @staff_member_required
# def ajax_upload_photos(request):  
#     try:attraction = Attraction.objects.get(id=request.GET['id'])
#     except:attraction=False
#     return upload_photos(request,AttractionPhotos,attraction,'attraction',True,True,True)
"""
@staff_member_required
def ajax_upload_photos(request):
    if request.method == "POST":
        gal_id = request.POST.get('gal_id')
        if gal_id and gal_id.isdigit():
            album = PhotoAlbum.objects.get(id=gal_id)
        else:
            attraction = Attraction.objects.get(id=request.GET['id'])
            album = PhotoAlbum()
            album.created_by = request.user
            album.category = attraction_album_cat
            album.is_editable = False
            album.status = 'N'
            album.title = attraction.name
            album.slug = getUniqueValue(PhotoAlbum, slugify(attraction.slug))
            album.seo_title = attraction.name[:70],
            album.seo_description = album.summary = attraction.description[:160]
            album.save()
            attraction.album = album
            attraction.save()
        response = upload_photos_forgallery(request,Photos,album,'album')
        album.save()
        return response
    else:
        attraction = Attraction.objects.get(id=request.GET['id'])
        album = attraction.album
        return upload_photos_forgallery(request,Photos,album,'album')

@staff_member_required
def ajax_upload_photos(request):
    if request.method == "POST":
        gal_id = request.POST.get('gal_id')
        aid = request.GET.get('id')
        if gal_id and gal_id.isdigit():
            album = PhotoAlbum.objects.get(id=gal_id)
        elif aid and aid.isdigit():
            attr = Attraction.objects.get(id=aid)
            album = attr.album
        else:
            album = None
        response = upload_photos_forgallery(request,Photos,album,'album')
        return response
    else:
        attraction = Attraction.objects.get(id=request.GET['id'])
        album = attraction.album
        return upload_photos_forgallery(request,Photos,album,'album')
"""    
    
def ajax_upload_photos(request):
    if request.method == "POST":
        attraction = Attraction.objects.get(id=request.GET['id'])
        if attraction.album:
            album = attraction.album
        else:
            title = request.POST.get('title', "").strip()
            if not title:
                try:
                    title = attraction.name
                except:
                    title = 'attractionAlbum-' + "".join(sample(rand, 10))
            album = PhotoAlbum(
               created_by=request.user,
               title=title,
               is_editable = False,
               slug=slugify(title),
               category=attraction_album_cat,
               seo_title=title[:70],
               status = 'N',
               seo_description=request.POST.get('eattraction_description', title)
            )
            album.save()
            attraction.album = album
        attraction.save()
        try:
            alllog = attraction.audit_log.all()
            log1 = alllog[0]
            log1.action_type = 'G'
            log1.save()
            log2 = alllog[1]
            
            if log1.action_type == log2.action_type and log1.modified_by == log2.modified_by:
                log1.delete()
        except:
            pass
        response = upload_photos_forgallery(request,Photos,album,'album')
        album.save()
        return response
    else:
        try:
            attraction = Attraction.objects.get(id=request.GET['id'])
            album = attraction.album
            return upload_photos_forgallery(request,Photos,album,'album')    
        except:
            return HttpResponse('No Object')




@staff_member_required
def ajax_upload_photos_preview(request):  
#     try:attraction = Attraction.objects.get(id=request.GET['id'])
#     except:attraction=False
#     return upload_photos(request,AttractionPhotos,attraction,'attraction',True,True)
    ""

# @staff_member_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,AttractionPhotos,pk) 

@staff_member_required
def attraction_photos(request,pk,template='attraction/staff/photos.html'):
    attraction = Attraction.objects.get(id = pk)
    data={'attraction':attraction}
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def change_photo_status_attraction(request):
#     try:
#         photo=AttractionPhotos.objects.get(id=int(request.GET['id']))
#         if request.user.has_perm('attraction.change_attraction'):
#             photo.is_approved=True
#             photo.save()
#             return HttpResponse('1')
#         else:return HttpResponse('0')
#     except:return HttpResponse('0')
    ""
    
@staff_member_required
def attraction_videos(request, template = 'attraction/staff/attraction-videos.html'):
    try:attraction = Attraction.objects.prefetch_related('attraction_video').get(id = request.GET['aid'])
    except:return HttpResponseRedirect(reverse('staff_manage_attraction'))
    data = {'attraction':attraction}
    return render_to_response(template, data, context_instance = RequestContext(request))

@staff_member_required
def attraction_add_videos(request, template='attraction/staff/attraction-videos-list.html'):
    data={}
    try:
        attraction = Attraction.objects.get(id = request.GET['aid'])
        video = AttractionVideos(attraction = attraction)
        is_vimeo = request.GET.get('is_vimeo','false')
        title = request.GET['title']
        if not title:title = attraction.name
        video.title = title
        video.video_url = request.GET['vid']
        video.added_by = request.user
        if is_vimeo != 'false':
            video.is_vimeo = True
            video.vimeo_image = request.GET['image']
        video.save()
        data['status'] = True
        attraction = Attraction.objects.prefetch_related('attraction_video').get(id = request.GET['aid'])
        html=render_to_string(template,{'attraction':attraction})
        data['html'] = html
    except:
        data['status'] = False
    return HttpResponse(simplejson.dumps(data))        
    
@staff_member_required    
def attraction_delete_videos(request):
    data = {}
    try:
        attraction = Attraction.objects.get(id = request.GET['aid'])
        video = AttractionVideos.objects.get(id=request.GET['vid'],attraction = attraction)
        video.delete()
        data['status'] = True
        data['total_videos'] = AttractionVideos.objects.filter(attraction = attraction).count()
    except:
        data['status'] = False
    return HttpResponse(simplejson.dumps(data))  
