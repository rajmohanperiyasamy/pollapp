import datetime
from time import strptime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
from django.template import Context
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages

from common.templatetags.ds_utils import get_msg_class_name
from common.models import GallerySettings
from common.staff_messages import GALLERY_MSG,COMMON
from common.getunique import getUniqueValue
from common.staff_utils import error_response
from common.utils import ds_pagination
from common.flickr import flickr
from common.mail_utils import mail_publish_gallery


from gallery.utils import save_gallery_tags
from gallery.forms import GalleryForm,GallerySEOForm
from gallery.models import PhotoCategory,PhotoAlbum,Photos,Tag as GalleryTag
from common import signals

NO_OF_ITEMS_PER_PAGE=10

###################  GALLERY ####################
@staff_member_required
def manage_gallery(request,template='gallery/staff/home.html'):
    gallery = PhotoAlbum.objects.filter(~Q(status='D')&Q(category__is_editable=True)).select_related('category','created_by').order_by('-created_on')
    gallery_state = PhotoAlbum.objects.filter(category__is_editable=True).values('status').annotate(s_count=Count('status')).exclude(status='D')
    
    page = int(request.GET.get('page',1))
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    for st in gallery_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(gallery,page,'gallery',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =GALLERY_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['categories'] = PhotoCategory.objects.filter(is_editable=True).order_by('name')
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['drafted'] =STATE['D']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['search'] =False
    try:data['recent'] = request.GET['pending_photos']
    except:data['recent'] = False
    try:data['gallery_settings']=GallerySettings.objects.all()[:1][0]
    except:pass
    return render_to_response(template,data, context_instance=RequestContext(request))


@staff_member_required
def ajax_list_gallery(request,template='gallery/staff/ajax_listing.html'):
    data=filter_gallery(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']=0-0
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))


@staff_member_required
def ajax_gallery_action(request,template='gallery/staff/ajax_delete_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    gallerylist = PhotoAlbum.objects.filter(id__in=id,category__is_editable=True)
    cls_count=gallerylist.count()
    status=0
    if action=='DEL':
        if request.user.has_perm('gallery.delete_photoalbum'):
            signals.celery_delete_indexs.send(sender=None,objects=gallerylist)
            gallerylist.delete()
            status=1
            msg=str(GALLERY_MSG['ADS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if action=='True' or action=='False':
            if request.user.has_perm('gallery.promote_photoalbum'):
                if action=='True':
                    action=True
                    gallerylist.update(is_featured=action,modified_by=request.user)
                    status=1
                    msg=str(GALLERY_MSG['AFSCS'])
                    for gallery in gallerylist:
                        gallery.save()
                else:
                    action=False
                    gallerylist.update(is_featured=action,modified_by=request.user)
                    status=1
                    msg=str(GALLERY_MSG['AFSNCS'])
                    for gallery in gallerylist:
                        gallery.save()
                mtype=get_msg_class_name('s')
            else:
                msg=str(COMMON['DENIED'])
                mtype=get_msg_class_name('w')
        else:
            if request.user.has_perm('gallery.publish_photoalbum'):
                gallerylist.update(status=action)
                if action=='P':
                    gallerylist.update(published_on=datetime.datetime.now())
                    try:
                        for gallery in gallerylist:mail_publish_gallery(gallery)
                    except:pass
                status=1
                msg=str(GALLERY_MSG['ASCS'])
                mtype=get_msg_class_name('s')
            else:
                msg=str(COMMON['DENIED'])
                mtype=get_msg_class_name('w')
    if action!='DEL':signals.celery_update_indexs.send(sender=None,objects=gallerylist)
    data=filter_gallery(request)
    new_id=[]
    for gallery in gallerylist:
        gallery.save()
        for log in gallery.audit_log.all()[:1]:
            if action == True:log.action_type = 'P'
            elif action == False:log.action_type = 'N'
            else:log.action_type = action
            log.save()
            
    for cs in data['gallery']:new_id.append(int(cs.id))
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

   
def filter_gallery(request):
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
            categorys = PhotoCategory.objects.get(id=search_category)
            key['category'] = categorys
        
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='desc':key['summary__icontains'] = search_keyword
            elif search_type=='postedby':key['created_by__display_name__icontains'] = search_keyword
        
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(summary__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if len(args) == 0 :gallery = PhotoAlbum.objects.filter(~Q(status='D')&Q(category__is_editable=True),q,**key).select_related('category','created_by').order_by(sort)
            else:gallery = PhotoAlbum.objects.filter(~Q(status='D')&Q(category__is_editable=True),q,**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :gallery = PhotoAlbum.objects.filter(~Q(status='D')&Q(category__is_editable=True),**key).select_related('category','created_by').order_by(sort)
            else:gallery = PhotoAlbum.objects.filter(~Q(status='D')&Q(category__is_editable=True),**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :gallery = PhotoAlbum.objects.filter(~Q(status='D')&Q(category__is_editable=True),**key).select_related('category','created_by').order_by(sort)
        else:gallery = PhotoAlbum.objects.filter(~Q(status='D')&Q(category__is_editable=True),args,**key).select_related('category','created_by').order_by(sort)
    
    gallery=gallery.distinct()
    data = ds_pagination(gallery,page,'gallery',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    if search:
        data['catgy'] = search_category
    data['item_perpage']=item_perpage
    return data 

@staff_member_required
@permission_required('gallery.publish_photoalbum',raise_exception=True)
def change_status_gallery(request):
    try:
        gallery=PhotoAlbum.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        gallery.status = status
        if status=='P':
            gallery.published_on=datetime.datetime.now()
            gallery.status = status
            try:mail_publish_gallery(gallery)
            except:pass
        gallery.save()
        for log in gallery.audit_log.all()[:1]:
            log.action_type = status
            log.save()
        signals.celery_update_index.send(sender=None,object=gallery)
        html ='<span title="'+gallery.get_status().title()+'" name="'+gallery.status+'" id="id_estatus_'+str(gallery.id)+'" class="inline-block status-idty icon-'+gallery.get_status()+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')

@staff_member_required
def ajax_gallery_state(request,template='gallery/staff/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
   
    if status == 'all':
        gallery_state = PhotoAlbum.objects.filter(category__is_editable=True).values('status').annotate(s_count=Count('status')).exclude(status='D')
    else:
        gallery_state = PhotoAlbum.objects.filter(category__is_editable=True,created_by=request.user).values('status').annotate(s_count=Count('status')).exclude(status='D')

    for st in gallery_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
        
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B']
    }
    return HttpResponse(simplejson.dumps(data)) 

"""
####################################################################################################
##############################################    ADD ##############################################
####################################################################################################
"""

@staff_member_required
@permission_required('gallery.add_photoalbum',raise_exception=True)
def add_gallery(request,template='gallery/staff/gallery_lightbox_holder.html'):
    form=GalleryForm()
    if request.method=='POST':
        form=GalleryForm(request.POST)
        if form.is_valid():
            gallery=form.save(commit=False)
            gallery.slug=getUniqueValue(PhotoAlbum,slugify(gallery.title))
            gallery.seo_title= gallery.title
            gallery.seo_description= gallery.summary[:160]
            gallery.created_by=gallery.modified_by=request.user
            gallery.status='N'
            gallery.is_featured=False
            gallery.save()
            #messages.success(request, str(GALLERY_MSG['AAS']))
            save_gallery_tags(gallery,request.POST['tags']) 
            return HttpResponseRedirect(reverse('staff_add_gallery_add_photos',args=[gallery.id]))
        else:
            data={'form':form}
            html=render_to_string(template, data, context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'html':html,'status':1}),mimetype='application/json')
    data={'form':form}
    return render_to_response(template, data, context_instance=RequestContext(request))


@staff_member_required
@permission_required('gallery.change_photoalbum',raise_exception=True)
def gallery_update(request,id,template='gallery/staff/update-gallery.html'):
    gallery=PhotoAlbum.objects.get(id=id)
    form=GalleryForm(instance=gallery)
    if request.method=='POST':
        form=GalleryForm(request.POST,instance=gallery)
        if form.is_valid():
            gallery=form.save(commit=False)
            gallery.slug=getUniqueValue(PhotoAlbum,slugify(gallery.title),instance_pk=gallery.id)
            gallery.modified_by=request.user
            gallery.save()
            save_gallery_tags(gallery,request.POST['tags'])
            detail=request.POST.get('detail',False)
            if not detail:
                messages.success(request, str(GALLERY_MSG['AUS']))
            data={'msg':str(GALLERY_MSG['AUS']),'mtype':get_msg_class_name('s'),'status':1}
            signals.celery_update_index.send(sender=None,object=gallery)
            if detail:
                html=render_to_string('gallery/staff/gallery_detail_content.html',{'gallery':gallery},context_instance=RequestContext(request))
                data['html']=html
            return HttpResponse(simplejson.dumps(data),mimetype='application/json')
        else:
            data={'form':form,'gallery':gallery}
            html=render_to_string(template, data, context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'html':html,'status':0}),mimetype='application/json')
    data={'form':form,'gallery':gallery}
    return render_to_response(template, data, context_instance=RequestContext(request))

@staff_member_required
def add_gallery_add_photos(request,id,template='gallery/staff/upload-photos-flickr.html'):
    if not request.user.has_perm('gallery.add_photoalbum') and not request.user.has_perm('gallery.change_photoalbum'):
        raise PermissionDenied
    data={
          'id':id,
          'gallery':PhotoAlbum.objects.get(id=id)
    }
    if request.method=='POST':
        fids = request.POST['flickr_ids']
        gallery = PhotoAlbum.objects.get(id=id)
        pre_photo_ids = set(Photos.objects.filter(album=gallery).exclude(photo_url=None).values_list('id', flat=True))
        new_photo_ids = set()
        if fids:
            fids=fids.split(',')
            for fid in fids:
                photo = Photos.objects.filter(album=gallery, photo_url__contains=fid)
                if photo.exists():
                    new_photo_ids.add(photo[0].id)
                else:
                    fphoto = flickr.Photo(fid)
                    photo = Photos(album=gallery,is_active=True)
                    #photo.title = fphoto.title
                    photo.caption = fphoto.title
                    try:                  
                        if not photo.created_by:photo.created_by = request.user
                    except:photo.created_by = request.user
                    photo.modified_by=request.user
                    
                    photo.photo_id = fphoto.id
                    photo.key = fphoto.farm +"_"+ fphoto.server +"_"+ fphoto.secret;
                    photo.photo_url = "http://farm"+ fphoto.farm +".static.flickr.com/"+ fphoto.server +"/"+ fphoto.id +"_"+ fphoto.secret+"_m.jpg";
                    photo.owner_name = fphoto.owner.username
                    photo.status = 'N'
                    try:photo.published_on = datetime.datetime(*strptime(fphoto.datetaken, "%Y-%m-%d  %H:%M:%S")[:7])
                    except:photo.published_on = datetime.datetime.now()
                    photo.save()
                    new_photo_ids.add(photo.id)
        deleted_photo_ids = pre_photo_ids.difference(new_photo_ids)
        Photos.objects.filter(id__in=deleted_photo_ids).delete()
        return HttpResponseRedirect(reverse('staff_add_gallery_add_photo_details',args=[gallery.id]))
    gsettings=GallerySettings.get_obj()
    if gsettings:
        if gsettings.flickr_api_key and gsettings.flickr_api_secret:data['gsetting']=True
        else:data['gsetting']=False
    else:data['gsetting']=False 
    return render_to_response(template, data, context_instance=RequestContext(request))

@staff_member_required
def add_gallery_add_photo_details(request,id):
    if not request.user.has_perm('gallery.add_photoalbum') and not request.user.has_perm('gallery.change_photoalbum'):
        raise PermissionDenied
    data={}
    gallery = PhotoAlbum.objects.get(id=id)
    if request.method == 'POST':
        ps = Photos.objects.filter(album=gallery)
        photos=[]
        for p in ps:
            try:
                description = request.POST['description_%d'%(p.id)]
                p.caption = description[:200]
                p.status = 'P'
                p.save()
                photos.append(p)
            except:pass
        gallery.save()
        for log in gallery.audit_log.all()[:1]:
            log.action_type='G'
            log.save()
        data={'msg':str(GALLERY_MSG['AAS']),'mtype':get_msg_class_name('s'),'status':1}
        detail=request.POST.get('detail',False) 
        if detail:
            html=render_to_string('gallery/staff/load_gallery.html',{'photos':photos},context_instance=RequestContext(request))
            data['html']=html
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    else:
        data['photos'] = Photos.objects.filter(album=gallery)
        data['gallery']=gallery
        return render_to_response('gallery/staff/describe-upload.html',data, RequestContext(request))


@staff_member_required
@permission_required('gallery.change_photoalbum',raise_exception=True)
def seo(request,id,template='gallery/staff/update_seo.html'):
    gallery = PhotoAlbum.objects.get(id = id)
    form=GallerySEOForm(instance=gallery)
    if request.POST:
        form=GallerySEOForm(request.POST,instance=gallery)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug=getUniqueValue(PhotoAlbum,slugify(seo.slug),instance_pk=seo.id)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(GALLERY_MSG['ASUS'])}))
        else:
            data={'form':form,'gallery':gallery}
            return error_response(request,data,template,GALLERY_MSG)
    data={'form':form,'gallery':gallery}
    return render_to_response(template,data, context_instance=RequestContext(request))


@staff_member_required
def gallery_detail(request,id,template='gallery/staff/detail.html'):
    gallery = PhotoAlbum.objects.get(id = id)
    photos=Photos.objects.filter(album=gallery)
    data={'gallery':gallery,'photos':photos}
    try:data['gallery_settings']=GallerySettings.objects.all()[:1][0]
    except:pass
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('gallery.change_photoalbum',raise_exception=True)
def gallery_photo_detail(request,id,template='gallery/staff/update_photo.html'):
    photo=Photos.objects.get(id = id)
    data={'photo':photo}
    if request.method=='POST':
        #photo.title=request.POST['summary'][:200]
        photo.caption=request.POST['summary'][:200]
        #photo.summary=request.POST['summary'][:200]
        if photo.status == 'N':
            photo.status = 'P'
        photo.save()
        html=render_to_string('gallery/staff/load_gallery.html',{'photo':photo},context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({'html':html,'mtype':get_msg_class_name('s'),'msg':str(GALLERY_MSG['APUS'])}))
    return render_to_response(template,data,context_instance=RequestContext(request))


@staff_member_required
def gallery_photo_delete(request):
    try:
        photo=Photos.objects.get(id = int(request.GET['id']))
        photo.delete()
        return HttpResponse(simplejson.dumps({'status':1,'msg':str(GALLERY_MSG['APDS']),'mtype':get_msg_class_name('s')}))
    except:return HttpResponse(simplejson.dumps({'status':0,'msg':str(GALLERY_MSG['OOPS']),'mtype':get_msg_class_name('e')}))


"""
###########################################################################################################################
#############################################         COMMON FUNCTION     #################################################
###########################################################################################################################
"""

from common.fileupload import upload_photos_forgallery,delete_photos

@login_required
def ajax_upload_photos(request):  
    album = PhotoAlbum.objects.get(id=request.REQUEST['id'])
    before = album.audit_log.all().count()
    response = upload_photos_forgallery(request,Photos,album,'album')
    after = album.audit_log.all().count()
    if after > before:
        album.audit_log.all()[0].delete()
    return response

@login_required
def ajax_delete_photo(request,pk):
    return delete_photos(request,Photos,pk) 

@login_required
def auto_suggest_tag(request):
    try:
        data = GalleryTag.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:
        data = GalleryTag.objects.all()[:10]
    child_dict = []
    for tag in data :
        buf={'label':tag.tag,'id':tag.id,'value':tag.tag}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), mimetype='application/javascript')


@login_required
def ajax_update_photo_caption(request, pk, template = 'common/update-photo-caption.html'):
    from common.fileupload import update_photo_caption
    data = {}
    photo = Photos.objects.get(id=pk)
    data['photo'] = photo
    data['html'] = template
    if request.method == 'POST':
        return update_photo_caption(request, photo) #calling method wriiten in common/fileupload.py
    try:
        if request.GET['user']:
            return render_to_response("common/user_update_caption_form.html", data, context_instance=RequestContext(request))
    except:
        pass
    return render_to_response(template,data, context_instance=RequestContext(request))


@staff_member_required
def set_cover_image(request,template='gallery/staff/set_cover_image.html'):
    data = {}
    album = PhotoAlbum.objects.get(id=int(request.REQUEST['gid']))
    data['album'] = album
    if request.method == 'POST':
        photos = album.get_gallery_image()
        photos.update(featured=False)
        pid = request.POST['pid']
        photo = Photos.objects.get(id=pid)
        photo.featured = True
        photo.save()
        return HttpResponse("Success")
    else:
        return render_to_response(template,data, context_instance=RequestContext(request))
        
