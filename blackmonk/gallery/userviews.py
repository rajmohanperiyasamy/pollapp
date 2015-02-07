import datetime
from time import strptime
import urllib
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages

from common.templatetags.ds_utils import get_msg_class_name
from common.models import GallerySettings,ApprovalSettings
from common.user_messages import GALLERY_MSG
from common.getunique import getUniqueValue
from common.utils import ds_pagination
from common.flickr import flickr
from common.mail_utils import mail_publish_gallery
from common.staff_utils import error_response

from gallery.utils import save_gallery_tags
from gallery.forms import UserGallerySEOForm
from gallery.forms import UserGalleryForm as GalleryForm
from gallery.models import PhotoCategory,PhotoAlbum,Photos,Tag as GalleryTag
from common import signals

NO_OF_ITEMS_PER_PAGE=10
status_dict = {
    'Rejected': 'R',
    'Draft': 'D',
    'Published': 'P',
    'Expired': 'E',
    'Pending': 'N',
    'Blocked': 'B',
}

###################  GALLERY ####################
@login_required
def manage_gallery(request,template='gallery/user/content_manager.html'):
    show = request.GET.get('show', None)
    if show is None:
        gallery = PhotoAlbum.objects.filter(created_by=request.user,category__is_editable=True).select_related('category','created_by').order_by('-created_on')
    else:
        gallery = PhotoAlbum.objects.filter(status=status_dict[show], created_by=request.user,category__is_editable=True).select_related('category','created_by').order_by('-created_on')
    gallery_state = PhotoAlbum.objects.values('status').filter(created_by=request.user,category__is_editable=True).annotate(s_count=Count('status'))
    
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
    data['categories'] = PhotoCategory.objects.all().order_by('name')
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['drafted'] =STATE['D']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['search'] =False
    try:data['gallery_settings']=GallerySettings.objects.all()[:1][0]
    except:pass
    if show is not None:
        data['show'] = status_dict[show]
    return render_to_response(template,data, context_instance=RequestContext(request))


@login_required
def ajax_list_gallery(request,template='gallery/user/ajax_object_listing.html'):
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


@login_required
def ajax_gallery_action(request,template='gallery/user/ajax_object_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    action=request.GET['action']
    gallery = PhotoAlbum.objects.filter(id__in=id)
    cls_count=gallery.count()
    
    if action=='DEL':
        for gall_del in gallery:
            signals.celery_delete_index.send(sender=None,object=gall_del)
            signals.create_notification.send(sender=None,user=request.user, obj=gall_del, not_type='deleted from',obj_title=gall_del.title)
        gallery.delete()
        msg=str(GALLERY_MSG['ADS'])
        mtype=get_msg_class_name('s')
    else:
        if action=='True' or action=='False':
            if action=='True':action=True
            else:action=False
            gallery.update(is_featured=action)
            msg=str(GALLERY_MSG['AFSCS'])
            mtype=get_msg_class_name('s')
        else:
            gallery.update(status=action)
            msg=str(GALLERY_MSG['ASCS'])
            mtype=get_msg_class_name('s')
    data=filter_gallery(request)
    if action!='DEL':signals.celery_update_indexs.send(sender=None,objects=gallery)

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
    send_data['total'] = PhotoAlbum.objects.filter(created_by=request.user,category__is_editable=True).count()
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))

def gallery_submit(request):
    try:
        gallery = PhotoAlbum.objects.get(id=request.GET.get('gid'))
        gallery.status = 'N'
        gallery.save()
        signals.celery_update_index.send(sender=None,object=gallery)
        signals.create_notification.send(sender=None,user=request.user, obj=gallery, not_type='updated in',obj_title=gallery.title)
        send_data = {'status': True}
    except:
        send_data = {'status': False}
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
    
    if listing_type == 'F':
        is_featured = True
        key['is_featured'] = is_featured
    elif listing_type == 'B':
        is_featured = False
        key['is_featured'] = is_featured
        
    if status!='all' and status!='':key['status'] = status

    key['created_by'] = request.user
    key['category__is_editable'] = True


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
        
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(summary__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if len(args) == 0 :gallery = PhotoAlbum.objects.filter(q,**key).select_related('category','created_by').order_by(sort)
            else:gallery = PhotoAlbum.objects.filter(q,**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :gallery = PhotoAlbum.objects.filter(~Q(status='D'),**key).select_related('category','created_by').order_by(sort)
            else:gallery = PhotoAlbum.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :gallery = PhotoAlbum.objects.filter(**key).select_related('category','created_by').order_by(sort)
        else:gallery = PhotoAlbum.objects.filter(args,**key).select_related('category','created_by').order_by(sort)
    
    gallery=gallery.distinct()
    data = ds_pagination(gallery,page,'gallery',item_perpage)
    data['status'] = status
    if search:
        data['search_keyword'] = request.GET.get('kwd',"").strip()
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

@login_required
def ajax_gallery_state(request,template='gallery/user/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
   
    if status == 'all':
        gallery_state = PhotoAlbum.objects.values('status').annotate(s_count=Count('status'))
    else:
        gallery_state = PhotoAlbum.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

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

@login_required
def add_gallery(request,template='gallery/user/add_gallery.html'):
    form=GalleryForm()
    if request.method=='POST':
        form=GalleryForm(request.POST)
        if form.is_valid():
            gallery=form.save(commit=False)
            gallery.slug=getUniqueValue(PhotoAlbum,slugify(gallery.title))
            gallery.seo_title= gallery.title
            gallery.seo_description= gallery.summary[:160]
            gallery.created_by=gallery.modified_by=request.user
            gallery.status='D'
            gallery.is_featured=False
            gallery.save()
            save_gallery_tags(gallery,request.POST['tags']) 
            signals.create_notification.send(sender=None,user=request.user, obj=gallery, not_type='created in',obj_title=gallery.title)
            return HttpResponseRedirect(reverse('user_add_gallery_upload_photos',args=[gallery.id]))
        else:
            data={'form':form}
            html=render_to_string(template, data, context_instance=RequestContext(request))
            return render_to_response(template, data, context_instance=RequestContext(request))
    data={'form':form}
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
def gallery_update(request,id,template='gallery/user/update_gallery.html'):
    gallery=PhotoAlbum.objects.get(id=id)
    form=GalleryForm(instance=gallery)
    if request.method=='POST':
        form=GalleryForm(request.POST,instance=gallery)
        if form.is_valid():
            gallery=form.save(commit=False)
            gallery.slug=getUniqueValue(PhotoAlbum,slugify(gallery.title),instance_pk=gallery.id)
            gallery.created_by=request.user
            sendsignal=False
            if gallery.status=='P':
                sendsignal=True
                try:
                    appreoval_settings = ApprovalSettings.objects.get(name='gallery')
                    if appreoval_settings.free_update:
                        gallery.status='P'
                        if not gallery.published_on:gallery.published_on=datetime.datetime.now()
                    else:gallery.status='N'
                except:gallery.status='N'
            gallery.save()
            if gallery.status=='P':
                mail_publish_gallery(gallery)
            save_gallery_tags(gallery,request.POST['tags'])
            signals.celery_update_index.send(sender=None,object=gallery)
            detail=request.POST.get('detail',False) 
            #data={'msg':str(GALLERY_MSG['AUS']),'mtype':get_msg_class_name('s'),'status':1}
            messages.success(request, str(GALLERY_MSG['AUS']))
            signals.create_notification.send(sender=None,user=request.user, obj=gallery, not_type='updated in',obj_title=gallery.title)
            if sendsignal:signals.create_staffmail.send(sender=None,object=gallery,module='photos',action='U',user=request.user)
            if detail:
                html=render_to_string('gallery/user/gallery_detail_content.html',{'gallery':gallery},context_instance=RequestContext(request))
                data['html']=html
            return HttpResponseRedirect(reverse('user_manage_gallery'))
        else:
            data={'form':form,'gallery':gallery}
            html=render_to_string(template, data, context_instance=RequestContext(request))
            return render_to_response(template, data, context_instance=RequestContext(request))
    data={'form':form,'gallery':gallery}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def add_gallery_add_flickr_photos(request,id,template='gallery/user/upload-photos-flickr.html'):
    data={
          'id':id,
          'gallery':PhotoAlbum.objects.get(id=id)
    }
    gallery = PhotoAlbum.objects.get(id=id)
    #if gallery.get_gallery_uploaded_images():
        #return HttpResponseRedirect(reverse('user_add_gallery_upload_photos',args=[gallery.id]))
    if request.method=='POST':
        fids = request.POST.getlist('flicker_id_list')
        gallery = PhotoAlbum.objects.get(id=id)
        pre_photo_ids = set(Photos.objects.filter(album=gallery).exclude(photo_url=None).values_list('id', flat=True))
        new_photo_ids = set()
        if fids:
            for fid in fids:
                photo = Photos.objects.filter(album=gallery, photo_url__contains=fid)
                if photo.exists():
                    new_photo_ids.add(photo[0].id)
                else:
                    fphoto = flickr.Photo(fid)
                    photo = Photos(album=gallery,created_by=request.user,modified_by=request.user,is_active=True)
                    #photo.title = fphoto.title
                    photo.caption = fphoto.title
                    photo.photo_id = fphoto.id
                    photo.key = fphoto.farm +"_"+ fphoto.server +"_"+ fphoto.secret;
                    photo_url = "http://farm"+ fphoto.farm +".static.flickr.com/"+ fphoto.server +"/"+ fphoto.id +"_"+ fphoto.secret+"_l.jpg";
                    link = photo_url
                    f = urllib.urlopen(link)
                    myfile = f.geturl()
                    if 'photo_unavailable' in str(myfile):
                        photo.photo_url = "http://farm"+ fphoto.farm +".static.flickr.com/"+ fphoto.server +"/"+ fphoto.id +"_"+ fphoto.secret+"_m.jpg";
                    else:
                        photo.photo_url = "http://farm"+ fphoto.farm +".static.flickr.com/"+ fphoto.server +"/"+ fphoto.id +"_"+ fphoto.secret+"_l.jpg";
                    photo.owner_name = fphoto.owner.username
                    photo.status = 'N'
                    try:photo.published_on = datetime.datetime(*strptime(fphoto.datetaken, "%Y-%m-%d  %H:%M:%S")[:7])
                    except:photo.published_on = datetime.datetime.now()
                    photo.save()
                    new_photo_ids.add(photo.id)
            deleted_photo_ids = pre_photo_ids.difference(new_photo_ids)
            Photos.objects.filter(id__in=deleted_photo_ids).delete()
        if gallery.status=='D':
            try:
                appreoval_settings = ApprovalSettings.objects.get(name='gallery')
                if appreoval_settings.free:
                    gallery.status='P'
                    gallery.published_on=datetime.datetime.now()
                    try:mail_publish_gallery(gallery)
                    except:pass
                else:gallery.status='D'
            except:gallery.status='D'
        gallery.save()
        
        if gallery.status=='P':
            appreoval_settings = ApprovalSettings.objects.get(name='gallery')
            if appreoval_settings.free:
                signals.create_notification.send(sender=None,user=request.user, obj=gallery, not_type='updated with new photos in',obj_title=gallery.title)
        signals.celery_update_index.send(sender=None,object=gallery)
        return HttpResponseRedirect(reverse('user_add_gallery_add_photo_details',args=[gallery.id]))
    gsettings=GallerySettings.get_obj()
    if gsettings:
        if gsettings.flickr_api_key and gsettings.flickr_api_secret:data['gsetting']=True
        else:data['gsetting']=False
    else:data['gsetting']=False 
    try:data['gallery_settings']=GallerySettings.objects.all()[:1][0]
    except:pass
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
def add_gallery_add_photos(request,id,template='gallery/user/upload-photos.html'):
    data={
          'id':id,
          'gallery':PhotoAlbum.objects.get(id=id)
    }
    gallery = PhotoAlbum.objects.get(id=id)
    #if gallery.get_gallery_flicker_images():
        #return HttpResponseRedirect(reverse('user_add_gallery_add_photos',args=[gallery.id]))
    if request.method=='POST':
        if gallery.status=='D':
            try:
                appreoval_settings = ApprovalSettings.objects.get(name='gallery')
                if appreoval_settings.free:
                    gallery.status='P'
                    gallery.published_on=datetime.datetime.now()
                    try:mail_publish_gallery(gallery)
                    except:pass
                else:gallery.status='D'
            except:gallery.status='D'
        gallery.save()
        
        for log in gallery.audit_log.all()[:4]:
            if log.action_type=="U":
                log.delete()
        
        if gallery.status=='P':
            appreoval_settings = ApprovalSettings.objects.get(name='gallery')
            if appreoval_settings.free:
                signals.create_notification.send(sender=None,user=request.user, obj=gallery, not_type='updated with new photos in',obj_title=gallery.title)
        signals.celery_update_index.send(sender=None,object=gallery)
        return HttpResponseRedirect(reverse('user_add_gallery_add_photo_details',args=[gallery.id]))
    gsettings=GallerySettings.get_obj()
    if gsettings:
        if gsettings.flickr_api_key and gsettings.flickr_api_secret:data['gsetting']=True
        else:data['gsetting']=False
    else:data['gsetting']=False 
    try:data['gallery_settings']=GallerySettings.objects.all()[:1][0]
    except:pass
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
def add_gallery_add_photo_details(request,id):
    data={}
    gallery = PhotoAlbum.objects.get(id=id)
    if request.method == 'POST':
        if gallery.status=='D':
            gallery.status='N'
            gallery.save()
        if gallery.status=='P' or gallery.status=='N':
            signals.create_staffmail.send(sender=None,object=gallery,module='photos',action='A',user=request.user)
        ps = Photos.objects.filter(album=gallery)
        photos=[]
        for p in ps:
            try:
                description = request.POST['description_%d'%(p.id)]
                #p.title = description[:250]
                p.caption = description[:200]
                #p.summary = description[:350]
                p.status = 'P'
                p.save()
                photos.append(p)
            except:pass
       
        for log in gallery.audit_log.all()[:1]:
            if log.action_type=="U":
                log.delete()
        
        #data={'msg':str(GALLERY_MSG['ASS']),'mtype':get_msg_class_name('s'),'status':1}
        messages.success(request, str(GALLERY_MSG['ASS']))
        detail=request.POST.get('detail',False) 
        if detail:
            html=render_to_string('gallery/user/load_gallery.html',{'photos':photos},context_instance=RequestContext(request))
            data['html']=html
        return HttpResponseRedirect(reverse('user_manage_gallery'))
    else:
        data['photos'] = Photos.objects.filter(album=gallery)
        data['gallery']=gallery
        return render_to_response('gallery/user/describe-upload.html',data, RequestContext(request))


@login_required
def seo(request,id,template='usercp_seo_form.html'):
    gallery = PhotoAlbum.objects.get(id = id)
    form=UserGallerySEOForm(instance=gallery)
    if request.POST:
        form=UserGallerySEOForm(request.POST,instance=gallery)
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

@login_required
def gallery_detail(request,id,template='gallery/user/detail.html'):
    gallery = PhotoAlbum.objects.get(id = id)
    photos=Photos.objects.filter(album=gallery)
    data={'album':gallery,'photos':photos}
    try:data['gallery_settings']=GallerySettings.objects.all()[:1][0]
    except:pass
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def gallery_photo_detail(request,id,template='gallery/user/update_photo.html'):
    photo=Photos.objects.get(id = id)
    data={'photo':photo}
    if request.method=='POST':
        #photo.title=request.POST['title'][:250]
        photo.caption=request.POST['summary'][:350]
        if photo.status=='N':photo.status = 'P'
        photo.save()
        html=render_to_string('gallery/user/load_gallery.html',{'photo':photo},context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({'html':html,'mtype':get_msg_class_name('s'),'msg':str(GALLERY_MSG['APUS'])}))
    return render_to_response(template,data,context_instance=RequestContext(request))


@login_required
def gallery_photo_delete(request):
    try:
        photo=Photos.objects.get(id = int(request.GET['id']))
        photo.delete()
        return HttpResponse(simplejson.dumps({'status':1,'msg':str(GALLERY_MSG['APDS']),'mtype':get_msg_class_name('s')}))
    except:return HttpResponse(simplejson.dumps({'status':0,'msg':str(GALLERY_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

@login_required
def auto_suggest_tag(request):
    try:data = GalleryTag.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:data = GalleryTag.objects.all()[:10]
    child_dict = []
    for tag in data :
        buf={'label':tag.tag,'id':tag.id,'value':tag.tag}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), mimetype='application/javascript')


