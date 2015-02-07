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
from common.static_msg import PHOTOS_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category,response_to_save_settings
from common.admin_utils import save_emailsettings,get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.models import ModuleNames,ApprovalSettings,GallerySettings
from common.forms import ApprovalSettingForm,SEOForm,GallerySettingsForm
from usermgmt.decorators import admin_required

from gallery.models import PhotoCategory,PhotoAlbum,Photos
from gallery.forms import PhotoCategoryForm,PhotoCategorySeoForm

"""
#####################################################################################################################
##############################################        Gallery       #################################################
#####################################################################################################################
"""

@admin_required
def gallery_settings(request, template='admin/portal/gallery/settings.html'):
    approval=None
    featured=0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    
    photos_category=PhotoCategory.objects.all().count()
    no_ablem=PhotoAlbum.objects.all().count()
    no_photos = Photos.objects.all().count()
    PhotoAlbum_state = PhotoAlbum.objects.values('is_featured','status').annotate(s_count=Count('status'),f_count=Count('is_featured'))
    
    for st in PhotoAlbum_state:
        STATE[st['status']]+=st['s_count']
        if st['is_featured']:
            featured+=st['f_count']
    
    data={
          'no_photos':no_photos,
          'no_featured_photos':featured,
          'photos_category':photos_category,
          'no_ablem':no_ablem,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B']
    }
    try:
        approval = ApprovalSettings.objects.get(name='gallery')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    
    gallery=GallerySettings.objects.all()[:1]
    if gallery:gallery=gallery[0]
    else:gallery=None
    flicker_form=GallerySettingsForm(instance=gallery)
    try:seo = ModuleNames.get_module_seo(name='gallery')
    except:seo = ModuleNames(name='gallery')
    if request.method=='POST':
        ############################################
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        flicker_form=GallerySettingsForm(request.POST,instance=gallery)
        seo_form = SEOForm(request.POST)
        ############################################
        if approval_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='gallery'
            approvals.modified_by=request.user
            approvals.save()
        ############################################
        if flicker_form.is_valid():flicker_form.save()   
        if approval_form.is_valid() and flicker_form.is_valid() and seo_form.is_valid():
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            save_emailsettings(request,'photos')
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'flicker_form':flicker_form,'emailsettings':get_emailsettings('photos')}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/gallery/include_settings.html',PHOTOS_MSG)
            
        extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'flicker_form':flicker_form,'emailsettings':get_emailsettings('photos')}
        data.update(extra_data)
        return response_to_save_settings(request,False,data,'admin/portal/gallery/include_settings.html',PHOTOS_MSG)
       
    else:
        extra_data = {'seo':seo,'approval_form':approval_form,'flicker_form':flicker_form,'emailsettings':get_emailsettings('photos')}
        data.update(extra_data)
        return render_to_response (template, data, context_instance=RequestContext(request))


################################################## CATEGORY #########################################

@admin_required
def gallery_category(request, template='admin/portal/gallery/category.html'):
    category=PhotoCategory.objects.all()
    data={'category':category}
    try:data['msg']=PHOTOS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def gallery_category_update(request,template='admin/portal/gallery/update_category.html'):
    data={}
    cat=None
    try:
        cat = PhotoCategory.objects.get(id=request.REQUEST['id'])
        form = PhotoCategoryForm(instance=cat)
    except:form = PhotoCategoryForm()
    if request.method=='POST':
        if cat:form = PhotoCategoryForm(request.POST, instance=cat)
        else:form = PhotoCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if category.slug:category.slug = getUniqueValue(PhotoCategory,slugify(form.cleaned_data.get('slug')),instance_pk=category.id)
            else:category.slug = getUniqueValue(PhotoCategory,slugify(form.cleaned_data.get('name')),instance_pk=category.id)
            category.created_by = category.modified_by = request.user
            category.is_active = True
            category.save()
            if cat:
                category.is_editable = cat.is_editable
            else:
                category.is_editable = True
            form=PhotoCategoryForm()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('admin_portal_gallery_category_update')}
            return success_response_to_save_category(append_data,data,template,PHOTOS_MSG)
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,PHOTOS_MSG)
    else:
        data = {'form':form,'cat':cat}
        return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def gallery_category_delete(request):
    data=response_delete_category(request,PhotoCategory,PHOTOS_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def gallery_seo_category_update(request, template='admin/portal/gallery/update_category_seo.html'):
    try:seo = PhotoCategory.objects.get(id=int(request.REQUEST['id']))
    except:return HttpResponse(str(PHOTOS_MSG['CNF']))
    form=PhotoCategorySeoForm(instance=seo)
    if request.method=='POST':
        form = PhotoCategorySeoForm(request.POST,instance=seo)
        if form.is_valid():
            seo=form.save(commit=False)
            try:seo.slug = getUniqueValue(PhotoCategory,slugify(request.POST['slug']),instance_pk=seo.id)
            except:seo.slug = getUniqueValue(PhotoCategory,slugify(seo.name),instance_pk=seo.id)
            seo.save()
            data={'status':1,'msg':str(PHOTOS_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data = {'form':form,'seo':seo}
            return error_response(data,template,PHOTOS_MSG)
    data={'seo':seo,'form':form}
    return render_to_response (template, data, context_instance=RequestContext(request))


