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
from django.contrib.auth.decorators import login_required
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
from common.staff_messages import VIDEO_MSG
from common.getunique import getUniqueValue,getSlugData
from common.utils import ds_pagination,get_lat_lng
#from common.models import models
from common.models import ApprovalSettings,GallerySettings
from common.mail_utils import mail_publish_videos

#Module Files(models,forms etc...
from videos.utils import *
from videos.forms import UserAddVideoViaLinkForm,UserVideoSEOForm,VideoCategoryForm
from videos.models import VideoCategory,Videos,Keywords

from common import signals


ITEMS_PER_PAGE = 10
status_dict = {
    'Rejected': 'R',
    'Draft': 'D',
    'Published': 'P',
    'Expired': 'E',
    'Pending': 'N',
    'Blocked': 'B',
}

@login_required
def user_home_listing(request):
    show = request.GET.get('show', None)
    videocategory = VideoCategory.objects.all().order_by('name')
    if show is None:
        videodisplay = Videos.objects.filter(created_by=request.user).select_related('category').order_by('-created_on')
    else:
        videodisplay = Videos.objects.filter(status=status_dict[show], created_by=request.user).select_related('category').order_by('-created_on')
    video_state = Videos.objects.values('status').filter(created_by=request.user).annotate(s_count=Count('status'))
    
    msg = request.GET.get('msg',"")
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
    for st in video_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    
    data = ds_pagination(videodisplay,'1','videodisplay',ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =VIDEO_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['categories'] = videocategory
    data['total'] =total
    data['published'] =STATE['P']
    data['drafted'] =STATE['D']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['expired'] =STATE['E']
    data['search'] =False
    if show is not None:
        data['show'] = status_dict[show]
    return render_to_response('videos/user/content_manager.html', data ,context_instance=RequestContext(request))



@login_required
def user_ajax_display_video(request,template='videos/user/ajax_object_listing.html'):
    data=filter_videos(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    return HttpResponse(simplejson.dumps(send_data))


@login_required
def user_ajax_video_action(request,template='videos/user/ajax_object_listing.html'):  #
    ''' ajax method for performing actions(update status,delete) ''' 
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']

    action=request.GET['action']
    videos = Videos.objects.filter(id__in=id)
    video_count=videos.count()
    if action=='DEL':
        for vide_del in videos:
            signals.celery_delete_index.send(sender=None,object=vide_del)
            signals.create_notification.send(sender=None,user=request.user, obj=vide_del, not_type='deleted from',obj_title=vide_del.title)
        videos.delete()
        msg=str(VIDEO_MSG['VDS'])
        mtype=get_msg_class_name('s')
    data=filter_videos(request)
    

    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagenation']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['total'] = Videos.objects.filter(created_by=request.user).count()
    send_data['msg']=msg
    send_data['mtype']=mtype    
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
    
    if status!='all':
        key['status'] = status
        
    if listing_type == 'F':
        featured = True
        key['featured'] = featured  

    key['created_by'] = request.user
    if search:
        search_type = request.GET.get('type','-created_on')
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        if search_category:key['category__id'] = search_category
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(description__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if not created_user:videodisplay = Videos.objects.filter(q,**key).select_related('category').order_by(sort)
            else:videodisplay = Videos.objects.filter(q,**key).select_related('category').order_by(sort)
        else:
            if not created_user:videodisplay = Videos.objects.filter(**key).select_related('category').order_by(sort)
            else:videodisplay = Videos.objects.filter(**key).select_related('category').order_by(sort)
    else:
         if not created_user:videodisplay = Videos.objects.filter(**key).select_related('category').order_by(sort)
         else:videodisplay = Videos.objects.filter(**key).select_related('category').order_by(sort)   
    
    data = ds_pagination(videodisplay,page,'videodisplay',item_perpage)
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
def ajax_user_video_edit(request,template='videos/user/video_edit_form.html'):
    ''' ajax method for editing/updating a particular video ''' 
    video = Videos.objects.get(id=request.REQUEST['video_id'])
    form=UserAddVideoViaLinkForm(instance=video) 
    if request.POST:
        form=UserAddVideoViaLinkForm(request.POST,instance=video) 
        
        if form.is_valid():
            video_link = request.POST['yt_videos_id']
            vide_form=form.save(commit=False)
#            try:
#                v = video_link.split('v=')[1].split('&')[0]
#            except:
#                return HttpResponseRedirect(reverse('staff_video_home'))   
#            vide_form.video_id = v

            vide_form.video_id = request.POST['videocode']
            try:
                appreoval_settings = ApprovalSettings.objects.get(name='videos')
                if appreoval_settings.free_update and request.POST['status']=='P':
                    vide_form.status = 'P'
                    if not vide_form.published_on:vide_form.published_on=datetime.datetime.now()
                else:
                    try:
                        state = request.POST['status']
                        if state == 'D':vide_form.status = 'D'
                        else:vide_form.status = 'N'
                    except:vide_form.status = 'D'
            except:
                try:
                    tate = request.POST['status']
                    if state == 'D':vide_form.status = 'D'
                    else:vide_form.status = 'N'
                except:vide_form.status = 'D'
            vide_form.slug=getUniqueValue(Videos,slugify(vide_form.title),instance_pk=video.id)
            vide_form.save()
            if vide_form.status=='P':
                mail_publish_videos(vide_form)
            signals.celery_update_index.send(sender=None,object=vide_form)
            signals.create_notification.send(sender=None,user=request.user, obj=vide_form, not_type='updated in',obj_title=vide_form.title)
            signals.create_staffmail.send(sender=None,object=vide_form,module='videos',action='U',user=request.user)
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(VIDEO_MSG['EVUS'])}))
        else:
            print form.errors
            data={'form':form,'video':video}
            return error_response(request,data,template,VIDEO_MSG)
    data={'form':form,'video':video}
    return render_to_response(template,data, context_instance=RequestContext(request))    
  
@login_required
def add_video(request,template='videos/user/video_form.html'):
    data = {}
    gsettings=GallerySettings.get_obj()
    if gsettings:
        if gsettings.vimeo_api_key and gsettings.vimeo_api_secret:
            data['gsetting']=True
        else:
            data['gsetting']=False
    else:
        data['gsetting']=False 
    if request.method == "POST":
        try:
            vids = []
            video_ids = request.POST['video_ids']
            if video_ids!='':
                try:video_ids = video_ids.split(',')
                except:video_ids=video_ids
                for id in video_ids :
                    title =  request.POST['title_'+id]
                    description =  request.POST['description_'+id]
                    add_videos = Videos(created_by = request.user,modified_by = request.user)
                    add_videos.title=title[:150]
                    add_videos.slug = getUniqueValue(Videos,slugify(add_videos.title),instance_pk=add_videos.id)
                    add_videos.status = 'N'
                    add_videos.is_active = False
                    add_videos.video_id = str(id)
                    add_videos.description = description
                    add_videos.seo_description = description[:150]
                    add_videos.seo_title = title[:100]
                    try:add_videos.duration = request.POST['durations'+id].strip()
                    except:pass
                    add_videos.save()
                    vids.append(str(add_videos.id))
            vimeo_video_ids = request.POST['vimeo_video_ids']
            if vimeo_video_ids!='':
                try:vimeo_video_ids = vimeo_video_ids.split(',')
                except:vimeo_video_ids=vimeo_video_ids
                for id in vimeo_video_ids :
                    title =  request.POST['vimeo_title_'+id]
                    description =  request.POST['vimeo_description_'+id]
                    add_videos = Videos(created_by = request.user,modified_by = request.user)
                    add_videos.title=title[:150]
                    add_videos.slug = getUniqueValue(Videos,slugify(add_videos.title),instance_pk=add_videos.id)
                    add_videos.status = 'N'
                    try:add_videos.vimeo_image = request.POST['img_large'+id]
                    except:pass
                    add_videos.is_active = False
                    add_videos.video_id = str(id)
                    add_videos.description = description
                    add_videos.seo_description = description[:150]
                    add_videos.seo_title = title[:100]
                    add_videos.is_vimeo = True
                    try:add_videos.duration = request.POST['durations'+id].strip()
                    except:pass
                    add_videos.save()
                    vids.append(str(add_videos.id))
            return HttpResponseRedirect(reverse('user_video_edit_selected_video') + "?ids=" + ",".join(vids))
        except:
            data = msg = _('Some error occured during uploading')
        return HttpResponse(simplejson.dumps(data))
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required  
def edit_selected(request):
    data = {}
    categories = VideoCategory.objects.all()
    today=datetime.datetime.now()
    today_date=today.date()
    d=datetime.datetime.now()-timedelta(days=1)
    ids = request.REQUEST['ids'].split(',')
    videos = Videos.objects.filter(id__in=ids,created_by=request.user,created_on__gte=d).order_by('-id')

    if not request.POST:
        data['videos'] = videos
        data['ids'] = request.REQUEST['ids']
        data['categories'] = categories
        return render_to_response('videos/user/video_description_form.html',data, context_instance=RequestContext(request)) 
    else:
        categories = request.POST.getlist('video_category')
        for (i,v) in zip(categories,videos):
            category = VideoCategory.objects.get(id=i)
            v.category = category
            v.title = request.POST['title%d'%(v.id)]
            v.description =request.POST['description%d'%(v.id)]
            try:
                appreoval_settings = ApprovalSettings.objects.get(name='videos')
                if appreoval_settings.free:
                    v.status = 'P'
                    if not v.published_on:v.published_on=datetime.datetime.now()
                    try:mail_publish_videos(v)
                    except:pass
                else:v.status = 'N'
            except:v.status = 'N'
            v.save()
           
            for log in v.audit_log.all()[:1]:
                log.delete()
            
            signals.celery_update_index.send(sender=None,object=v)
            if v.status=='P' or v.status=='N':signals.create_staffmail.send(sender=None,object=v,module='videos',action='A',user=request.user)
            signals.create_notification.send(sender=None,user=request.user, obj= v, not_type='added in',obj_title= v.title)
        messages.success(request, str(VIDEO_MSG['YES'])) 
        return HttpResponseRedirect(reverse('user_video_home_listingboard')+'?msg=YES&mtype=s')

@login_required
def youtube_ajax_video_adding_user(request,template='videos/user/user-youtubeadd.html'):
    ''' ajax method used for adding videos from youtube'''  
    Videos.objects.filter(status='D',created_by=request.user).delete()
    data = {}
    try:
        add=request.GET['add']
    except:
        add=False
    if not add:
        try:
            video_ids = request.POST['video_ids']
            if video_ids!='':
                try:video_ids = video_ids.split(',')
                except:video_ids=video_ids
                for id in video_ids :
                    title =  request.POST['title_'+id]
                    description =  request.POST['description_'+id]
                    add_videos = Videos(created_by = request.user,modified_by = request.user)
                    add_videos.title=title[:150]
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
                    #messages.success(request, str(VIDEO_MSG['YES']))
                
            vimeo_video_ids = request.POST['vimeo_video_ids']
            if vimeo_video_ids!='':
                try:vimeo_video_ids = vimeo_video_ids.split(',')
                except:vimeo_video_ids=vimeo_video_ids
                for id in vimeo_video_ids :
                    title =  request.POST['vimeo_title_'+id]
                    description =  request.POST['vimeo_description_'+id]
                    add_videos = Videos(created_by = request.user,modified_by = request.user)
                    add_videos.title=title[:150]
                    add_videos.slug = getUniqueValue(Videos,slugify(add_videos.title),instance_pk=add_videos.id)
                    add_videos.status = 'D'
                    try:add_videos.vimeo_image = request.POST['img_large'+id]
                    except:pass
                    add_videos.is_active = False
                    add_videos.video_id = str(id)
                    add_videos.description = description
                    add_videos.seo_description = description[:150]
                    add_videos.seo_title = title[:100]
                    add_videos.is_vimeo = True
                    try:add_videos.duration = request.POST['durations'+id].strip()
                    except:pass
                    add_videos.save()
                    #messages.success(request, str(VIDEO_MSG['YES']))
            return HttpResponseRedirect(reverse('user_video_edit_selected_video'))        
        except:
            data = msg = _('Some error occured during uploading')
        return HttpResponse(simplejson.dumps(data))
    else:
        gsettings=GallerySettings.get_obj()
        if gsettings:
            if gsettings.vimeo_api_key and gsettings.vimeo_api_secret:data['gsetting']=True
            else:data['gsetting']=False
        else:data['gsetting']=False 
        return render_to_response(template,data, context_instance=RequestContext(request))
    
    
@login_required
def ajax_user_video_seo(request,template='usercp_seo_form.html'):
    ''' ajax method for editing/updating SEO of video ''' 
    video = Videos.objects.get(id=request.REQUEST['video_id'])
    form=UserVideoSEOForm(instance=video) 
    if request.POST:
        form=UserVideoSEOForm(request.POST,instance=video) 
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(VIDEO_MSG['VSUS'])}))
        else:
            data={'form':form,'video':video}
            return error_response(request,data,template,VIDEO_MSG)
    data={'form':form,'video':video}
    return render_to_response(template,data, context_instance=RequestContext(request))  

@login_required
def change_status(request):
    try:
        video=Videos.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        video.status = status
        video.save()
        signals.celery_update_index.send(sender=None,object=video)
        html ='<span title="'+video.get_video_status().title()+'" name="'+video.status+'" id="id_estatus_'+str(video.id)+'" class="inline-block status-idty icon-'+video.get_video_status()+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')

@login_required 
def vimeo_ajax_video_search(request):
    data=vimeo(request.GET['q'],40,request.GET['sort'],request.GET['page'])
    if data:return HttpResponse(simplejson.dumps(data)) 
    else:return HttpResponse('0')

def video_preview(request,slug):
    '''details of particular video'''
    data={}
    try:video = Videos.objects.prefetch_related('keywords').select_related('category','created_by').get(slug=slug)
    except:return HttpResponseRedirect(reverse('videos_videos_by_category'))
    
    '''method for counting views of particular video'''
    set_video_session(request,video)
    
    data['video'] = video
    return render_to_response('videos/user/preview.html',data, context_instance=RequestContext(request))


    