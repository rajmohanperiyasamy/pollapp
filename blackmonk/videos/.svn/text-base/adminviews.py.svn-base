#Python

#Django
from django.http import HttpResponseRedirect, HttpResponse 
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count


#Library
from common.static_msg import VIDEOS_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category
from common.admin_utils import response_to_save_settings,save_emailsettings,get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.models import ModuleNames,ApprovalSettings,GallerySettings
from common.forms import ApprovalSettingForm,SEOForm,VideoSettingsForm
from usermgmt.decorators import admin_required

from videos.models import VideoCategory,Videos
from videos.forms import VideoCategoryForm,VideoCategorySeoForm

"""
#####################################################################################################################
##############################################        VIDEOS        #################################################
#####################################################################################################################
"""
@admin_required
def videos_settings(request, template='admin/portal/videos/settings.html'):
    approval=None
    featured=0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    
    videos_category=VideoCategory.objects.all().count()
    no_videos=Videos.objects.all().count()
    videos_state = Videos.objects.values('status','featured').annotate(s_count=Count('status'),f_count=Count('featured'))
    
    for st in videos_state:
        STATE[st['status']]+=st['s_count']
        if st['featured']:
            featured+=st['f_count']
    
    data={
          'no_videos':no_videos,
          'no_featured_videos':featured,
          'videos_category':videos_category,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B']
    }
    gallery=GallerySettings.objects.all()[:1]
    if gallery:gallery=gallery[0]
    else:gallery=None
    if gallery:video_form=VideoSettingsForm(instance=gallery)
    else:video_form=VideoSettingsForm()
    try:
        approval = ApprovalSettings.objects.get(name='videos')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:seo = ModuleNames.get_module_seo(name='videos')
    except:seo = ModuleNames(name='videos')
    if request.method=='POST':
        ############################################
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        seo_form = SEOForm(request.POST)
        if gallery:video_form=VideoSettingsForm(request.POST,instance=gallery)
        else:video_form=VideoSettingsForm(request.POST)
        ############################################
        if video_form.is_valid():video_form.save()
        if approval_form.is_valid() and seo_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='videos'
            approvals.modified_by=request.user
            approvals.save()
            
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            
            ############################################
            save_emailsettings(request,'videos') 
            extra_data = {'video_form':video_form,'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('videos')}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/videos/include_settings.html',VIDEOS_MSG)
        else:
            extra_data = {'video_form':video_form,'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('videos')}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/videos/include_settings.html',VIDEOS_MSG)
    extra_data = {'video_form':video_form,'seo':seo,'approval_form':approval_form,'emailsettings':get_emailsettings('videos')}
    data.update(extra_data)
    return render_to_response (template, data, context_instance=RequestContext(request))
    

################################################## CATEGORY #########################################

@admin_required
def videos_category(request, template='admin/portal/videos/category.html'):
    category=VideoCategory.objects.order_by('name')
    data={'category':category}
    try:data['msg']=VIDEOS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def videos_category_update(request,template='admin/portal/videos/update_category.html'):
    data={}
    cat=None
    try:cat = VideoCategory.objects.get(id=request.REQUEST['id'])
    except:form = VideoCategoryForm()
    form = VideoCategoryForm(instance=cat)
    if request.method=='POST':
        if cat:form = VideoCategoryForm(request.POST,instance=cat)
        else:form = VideoCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            try:category.slug = getUniqueValue(VideoCategory,slugify(request.POST['slug']),instance_pk=category.id)
            except:category.slug =getUniqueValue(VideoCategory,slugify(request.POST['slug']))
            category.save()
            form=VideoCategoryForm()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('admin_portal_videos_category_update')}
            return success_response_to_save_category(append_data,data,template,VIDEOS_MSG)
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,VIDEOS_MSG)
    else:
        data = {'form':form,'cat':cat}
        return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def videos_category_delete(request):
    data=response_delete_category(request,VideoCategory,VIDEOS_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def videos_seo_category_update(request, template='admin/portal/videos/update_category_seo.html'):
    try:seo = VideoCategory.objects.get(id=int(request.REQUEST['id']))
    except:return HttpResponse(str(VIDEOS_MSG['CNF']))
    form=VideoCategorySeoForm(instance=seo)
    if request.method=='POST':
        form = VideoCategorySeoForm(request.POST,instance=seo)
        if form.is_valid():
            seo=form.save(commit=False)
            try:seo.slug = getUniqueValue(VideoCategory,slugify(request.POST['slug']),instance_pk=seo.id)
            except:seo.slug = getUniqueValue(VideoCategory,slugify(seo.name),instance_pk=seo.id)
            seo.save()
            data={'status':1,'msg':str(VIDEOS_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data = {'form':form,'seo':seo}
            return error_response(data,template,VIDEOS_MSG)
    data={'seo':seo,'form':form}
    return render_to_response (template, data, context_instance=RequestContext(request))
        

