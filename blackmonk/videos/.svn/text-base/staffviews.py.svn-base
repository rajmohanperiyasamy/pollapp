#Python Libs
from datetime import date, timedelta
from PIL import Image
from xml.dom import minidom
import os
import cgi
from urlparse import urlparse
import urllib
import re, urllib2

#Django Libs and Methods
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.template import Context, loader
from django.template import RequestContext
from django import forms
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.core.cache import cache
from django.conf import settings
from django.db.models import Count
from django.utils.translation import ugettext as _
from django.contrib import messages


#Application Libs and Common Methods
from common.templatetags.ds_utils import get_msg_class_name
from common.staff_utils import error_response
from common.staff_messages import VIDEO_MSG,COMMON
from common.getunique import getUniqueValue,getSlugData
from common.utils import ds_pagination,get_lat_lng
from common.models import GallerySettings
from common.mail_utils import mail_publish_videos
#Module Files(models,forms etc...
from videos.utils import *
from videos.forms import AddVideoViaLinkForm,VideoSEOForm,VideoCategoryForm
from videos.models import VideoCategory,Videos,Keywords
from common import signals

ITEMS_PER_PAGE = 10

#################################################################################NEW CODE#############################################Shaan

@staff_member_required
def display_video(request):
    ''' video home page functionalities '''
    data = {}
    item_perpage = int(request.GET.get('item_perpage',ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))
    
    videodisplay = Videos.objects.all().select_related('category','created_by__profile').exclude(status='D').order_by('-id')
    categories = VideoCategory.objects.order_by('name')
    video_state = Videos.objects.values('status').annotate(s_count=Count('status')).exclude(status='D')
    msg = request.GET.get('msg',"")
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0,'K':0}
    for st in video_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data = ds_pagination(videodisplay,page,'videodisplay',item_perpage)
    try:data['msg'] =VIDEO_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    
    data['categories'] = categories
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    data['data_type'] = True
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['total'] =total
    try:data['recent'] = request.GET['pending_videos']
    except:data['recent'] = False
    return render_to_response('videos/staff/video-home.html', data ,context_instance=RequestContext(request))

def ajax_display_video(request,template='videos/staff/ajax-video-listing.html'):
    ''' videos listing method(ajax) for displaying videos based on the parameters passed by user''' 
    
    data=filter_videos(request)
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
    return HttpResponse(simplejson.dumps(send_data))

def ajax_video_action(request,template='videos/staff/video-ajax-delete-listing.html'):  #
    ''' ajax method for performing actions(update status,delete) ''' 
    msg=mtype=''
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    videos = Videos.objects.filter(id__in=id)
    video_count=videos.count()
    status=0
    if action=='DEL':
        if request.user.has_perm('videos.delete_videos'):
            signals.celery_delete_indexs.send(sender=None,objects=videos)
            videos.delete()
            status=1
            msg=str(VIDEO_MSG['VDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
            
    if action=='F':
        if request.user.has_perm('videos.promote_videos'):
            videos.update(featured=True)
            status=1
            msg=str(VIDEO_MSG['FVS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    
    if action=='BAC' or action=='UF':
        if request.user.has_perm('videos.promote_videos'):
            videos.update(featured=False)
            status=1
            msg=str(VIDEO_MSG['UFVS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
            
    if request.user.has_perm('videos.publish_videos'):
        if action=='B':
            videos.update(status='B')
            msg=str(VIDEO_MSG['FBS'])
            mtype=get_msg_class_name('s')
        elif action=='P':
            try:
                for video in videos:mail_publish_videos(video)
            except:pass
            videos.update(status='P')
            videos.update(published_on=datetime.datetime.now())
            msg=str(VIDEO_MSG['VPS'])
            mtype=get_msg_class_name('s')
        elif action=='R':
             videos.update(status='R')
             msg=str(VIDEO_MSG['VRS'])
             mtype=get_msg_class_name('s')
        elif action=='N':
            videos.update(status='N')
            msg=str(VIDEO_MSG['VPES'])
            mtype=get_msg_class_name('s')
        status=1
    else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    if action!='DEL':signals.celery_update_indexs.send(sender=None,objects=videos)
    data=filter_videos(request)
    for video in videos:
        video.modified_by = request.user
        video.save()
        for log in video.audit_log.all()[:1]:
            if action == "BAC" or action == "UF":log.action_type = 'N'
            else : log.action_type = action
            log.save()
    new_id=[]
    for vid in data['videodisplay']:new_id.append(int(vid.id))
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
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype    
    send_data['status']=status 
    return HttpResponse(simplejson.dumps(send_data)) 

def filter_videos(request):
    ''' videos filtering functions based on status,created by,search'''
    data=key={}
    q=()
    created_user = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-created_on')
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    
    if status!='all' and status!='':
        key['status'] = status
    if listing_type != 'all':
        key['featured'] = True if listing_type == 'F' else False 

    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:created_user = True
    if search:
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        if search_category:key['category__id'] = search_category
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(description__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if not created_user:videodisplay = Videos.objects.filter(q,**key).exclude(status='D').select_related('category','created_by').order_by(sort)
            else:videodisplay = Videos.objects.filter(q,**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if not created_user:videodisplay = Videos.objects.filter(~Q(status='D'),**key).select_related('category','created_by').order_by(sort)
            else:videodisplay = Videos.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if not created_user:videodisplay = Videos.objects.filter(**key).exclude(status='D').select_related('category','created_by').order_by(sort)
        else:videodisplay = Videos.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)   
    
    data = ds_pagination(videodisplay,page,'videodisplay',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    if search:
        data['catgy']=search_category
    data['item_perpage']=item_perpage
    return data

@staff_member_required
@permission_required('videos.change_videos',raise_exception=True)
def ajax_video_edit(request,template='videos/staff/edit-video.html'):
    ''' ajax method for editing/updating a particular video ''' 
    video = Videos.objects.get(id=request.REQUEST['video_id'])
    form=AddVideoViaLinkForm(instance=video) 
    if request.POST:
        form=AddVideoViaLinkForm(request.POST,instance=video) 
        
        if form.is_valid():
            video_link = request.POST['yt_videos_id']
            vide_form=form.save(commit=False)
            try:
               v=video_link.split('v=')[1].split('&')[0]
            except:
                return HttpResponseRedirect(reverse('staff_video_home'))   
            vide_form.video_id = v     
            vide_form.slug=getUniqueValue(Videos,slugify(vide_form.title),instance_pk=video.id)
            vide_form.modified_by = request.user
            vide_form.save()
            signals.celery_update_index.send(sender=None,object=vide_form)
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(VIDEO_MSG['EVUS'])}))
        else:
            data={'form':form,'video':video}
            return error_response(request,data,template,VIDEO_MSG)
    data={'form':form,'video':video}
    return render_to_response(template,data, context_instance=RequestContext(request))    
        
@staff_member_required
@permission_required('videos.change_videos',raise_exception=True)
def ajax_video_seo(request,template='videos/staff/add-video-seo.html'):
    ''' ajax method for editing/updating SEO of video ''' 
    video = Videos.objects.get(id=request.REQUEST['video_id'])
    form=VideoSEOForm(instance=video) 
    if request.POST:
        form=VideoSEOForm(request.POST,instance=video) 
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(VIDEO_MSG['VSUS'])}))
        else:
            data={'form':form,'video':video}
            return error_response(request,data,template,VIDEO_MSG)
    data={'form':form,'video':video}
    return render_to_response(template,data, context_instance=RequestContext(request))   




#################################################################################NEW CODE ENDS#############################################

@staff_member_required
@permission_required('videos.add_videos',raise_exception=True)
def youtube_ajax_video_adding(request,template='videos/staff/youtubevideoadd.html'):
    ''' ajax method used for adding videos from youtube'''   
    Videos.objects.filter(status='D',created_by=request.user).delete()
    data = {}
    try:add=request.GET['add']
    except:add=False
    if not add:
        try:
            video_ids = request.POST.get('video_ids','')
            if video_ids!='':
                try:video_ids = video_ids.split(',')
                except:video_ids=video_ids
                for id in video_ids :
                    title =  request.POST['title_'+id]
                    description =  request.POST['description_'+id]
                    add_videos = Videos(created_by = request.user)
                    add_videos.title=title[:100]
                    add_videos.slug = getUniqueValue(Videos,slugify(add_videos.title),instance_pk=add_videos.id)
                    add_videos.status = 'D'
                    add_videos.is_active = False
                    add_videos.video_id = str(id)
                    add_videos.description = description
                    add_videos.seo_description = description[:150]
                    add_videos.seo_title = title[:100]
                    try:add_videos.duration = request.POST['durations'+id].strip()
                    except:pass
                    add_videos.save()
                
            vimeo_video_ids = request.POST.get('vimeo_video_ids','')
            if vimeo_video_ids!='':
                try:vimeo_video_ids = vimeo_video_ids.split(',')
                except:vimeo_video_ids=vimeo_video_ids
                for id in vimeo_video_ids :
                    title =  request.POST['vimeo_title_'+id]
                    description =  request.POST['vimeo_description_'+id]
                    add_videos = Videos(created_by = request.user)
                    add_videos.title=title[:100]
                    add_videos.slug = getUniqueValue(Videos,slugify(add_videos.title),instance_pk=add_videos.id)
                    add_videos.status = 'D'
                    add_videos.vimeo_image = request.POST['img_large'+id]
                    add_videos.is_active = False
                    add_videos.video_id = str(id)
                    add_videos.description = description
                    add_videos.seo_description = description[:150]
                    add_videos.seo_title = title[:100]
                    add_videos.is_vimeo = True
                    try:add_videos.duration = request.POST['durations'+id].strip()
                    except:pass
                    add_videos.save()
            
            return HttpResponseRedirect(reverse('staff_video_edit_selected_video'))        
        except:data = msg = _('Some error occured during uploading')
        return HttpResponse(simplejson.dumps(data))
    else:
        gsettings=GallerySettings.get_obj()
        if gsettings:
            if gsettings.vimeo_api_key and gsettings.vimeo_api_secret:data['gsetting']=True
            else:data['gsetting']=False
        else:data['gsetting']=False 
        return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('videos.delete_videos',raise_exception=True)
def video_ajax_deleting(request):
    data = {}
    video_id = request.GET.get('video_id',False)
    try:
        video = Videos.objects.get(id=video_id)
        signals.celery_delete_index.send(sender=None,object=video)
        video.delete()
        data={'status':1,'msg':'Video '+ video.title +' deleted successfully','mtype':get_msg_class_name('s'),'id':video_id}
    except:
        data={'status':0,'msg':str('Process Incomplete'),'mtype':get_msg_class_name('e')}
    return HttpResponse(simplejson.dumps(data))

 

@staff_member_required
def ajax_video_state(request):
    estatus = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0,'K':0}
    if estatus == 'all':
        video_state = Videos.objects.values('status').annotate(s_count=Count('status')).exclude(status='D')
    else:
        video_state = Videos.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status')).exclude(status='D')

    for st in video_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'status':estatus,
    }
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
@permission_required('videos.delete_videos',raise_exception=True)
def youtube_delete_list(request):
    id = request.GET.get('id','')
    data = {}
    try:    
        video_to_delete = Videos.objects.get(video_id=id)
        signals.celery_delete_index.send(sender=None,object=video_to_delete)
        video_to_delete.delete()
        data = msg = 'Done'
    except:
       data =  msg = "Couldn't Remove from the list "    

    return HttpResponse(simplejson.dumps(data))    

@staff_member_required
@permission_required('videos.change_videos',raise_exception=True)
def edit_selected_video(request):
    data = {}
    today=datetime.datetime.now()
    today_date=today.date()
    d=datetime.datetime.now()-timedelta(days=1)
    categories = VideoCategory.objects.all()
    videos = Videos.objects.filter(status='D',created_by = request.user,created_on__gte=d).order_by('-id')
    if not request.POST:
        data['videos'] = videos
        data['categories'] = categories
        return render_to_response('videos/staff/video-edit.html',data, context_instance=RequestContext(request)) 
    else:
        categories = request.POST.getlist('video_category')
        for (i,v) in zip(categories,videos):
            category = VideoCategory.objects.get(id=i)
            v.category = category
            v.title = request.POST['title%d'%(v.id)]
            v.description =request.POST['description%d'%(v.id)]
            v.status = 'N'
            if not v.created_by:v.modified_by = request.user
            if not v.published_on:v.published_on=datetime.datetime.now()
            v.save()
            #Delete unecessary logs which is created during adding of videos.
            for vlog in v.audit_log.all():
                if vlog.action_type=='U':
                    vlog.delete()
        messages.success(request, str(VIDEO_MSG['YES']))
                    
        return HttpResponseRedirect(reverse('staff_video_home')+'?msg=YES&mtype=s')
             
@staff_member_required
def seo_center(request,id,template='videos/staff/seo.html'):
    data = {}
    video = Videos.objects.get(id=id)
    data={'video':video}
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('videos.publish_videos',raise_exception=True)
def ajax_video_change_status(request):
    try:
        video=Videos.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        video.status = status
        if status=='P':
            video.published_on = datetime.datetime.now()
            try:mail_publish_videos(video)
            except:pass
        video.modified_by = request.user
        video.save()
        for log in video.audit_log.all()[:1]:
            log.action_type = status
            log.save()
        signals.celery_update_index.send(sender=None,object=video)
        html ='<span title="'+video.get_video_status().title()+'" name="'+video.status+'" id="id_estatus_'+str(video.id)+'" class="inline-block status-idty icon-'+video.get_video_status()+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')

def vimeo_ajax_video_search(request):
    data=vimeo(request.GET['q'],40,request.GET['sort'],request.GET['page'])
    if data:return HttpResponse(simplejson.dumps(data)) 
    else:return HttpResponse('0')
    
    