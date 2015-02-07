#Python

#Django
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.template.defaultfilters import slugify
#Library
from common.static_msg import LOCALITY_MSG
from common.admin_utils import error_response,response_delete_locality,success_response_to_save_locality
from common.templatetags.ds_utils import get_msg_class_name
from common.models import ModuleNames,ApprovalSettings,SocialSettings
from common.utils import ds_pagination,get_global_settings,get_lat_lng  
from usermgmt.decorators import admin_required
from common.getunique import getUniqueValue
from common.models import VenueType,Address,VenuePhoto
from locality.models import Zipcode
from locality.forms import ZipForm,VenueForm,VenueSeoForm,VenueTypeForm

"""
#####################################################################################################################
######################################        HOME      #########################################################
#####################################################################################################################
"""

@admin_required
def locality(request, template='admin/portal/locality/home.html'):
    zipcode=Zipcode.objects.all().count()
    venue=Address.objects.all().count()
    
    data={
          'zipcode':zipcode,
          'venue':venue
    }
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def locality_zipcode(request, template='admin/portal/locality/zipcode.html'):
    zipcode=Zipcode.objects.all().order_by('zip')
    try:page=int(request.GET['page'])
    except:page=1
    data = ds_pagination(zipcode,page,'zipcode',30)
    data['url'] = reverse('admin_portal_locality_zipcode')
    try:data['msg']=LOCALITY_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def locality_zipcode_ajax(request, template='admin/portal/locality/include_zipcode.html'):
    zipcode=Zipcode.objects.all().order_by('zip')
    try:page=int(request.GET['page'])
    except:page=1
    data = ds_pagination(zipcode,page,'zipcode',30)
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def locality_zipcode_update(request,template='admin/portal/locality/update_zipcode.html'):
    data={}
    zipcode=None
    try:
        zipcode=Zipcode.objects.get(id=int(request.REQUEST['id']))
        form=ZipForm(instance=zipcode)
    except:form=ZipForm()
    if request.method=='POST':
        if zipcode:form=ZipForm(request.POST,instance=zipcode)
        else:
            try:
                Zipcode.objects.get(zip__iexact=request.REQUEST['zip'])
                raise forms.ValidationError("The zip '" + request.REQUEST['zip'] + "' already added")
            except:
                form=ZipForm(request.POST)
        if form.is_valid():
            zip=form.save(commit=False)
            try:
                zip.latitude, zip.longitude, zip.zoom = get_lat_lng(request.POST['lat_lng'])
                try:zip.zoom = int(request.POST['zoom'])
                except:pass
            except:zip.latitude, zip.longitude, zip.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            zip.save() 
            form=ZipForm()
            data = {'form':form,'zipcode':zipcode}
            append_data={'cat':zip,'edit_url':reverse('admin_portal_locality_zipcode_update')}
            return success_response_to_save_locality(append_data,data,template,LOCALITY_MSG)
        else:
            data = {'form':form,'zipcode':zipcode}
            return error_response(data,template,LOCALITY_MSG)
    else:
        data = {'form':form,'zipcode':zipcode}
        return render_to_response (template, data, context_instance=RequestContext(request))
    
@admin_required
def locality_zipcode_delete(request):
    data=response_delete_locality(request,Zipcode,LOCALITY_MSG,'Z')
    return HttpResponse(simplejson.dumps(data))

######################################################################################################################
######################################################################################################################
######################################################################################################################

@admin_required
def locality_venuetype(request, template='admin/portal/locality/venuetype.html'):
    venuetype=VenueType.objects.all().order_by('title')
    try:page=int(request.GET['page'])
    except:page=1
    data = ds_pagination(venuetype,page,'venuetype',30)
    data['url'] = reverse('admin_portal_locality_venuetype')
    try:data['msg']=LOCALITY_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def locality_venuetype_ajax(request, template='admin/portal/locality/include_venuetype.html'):
    venuetype=VenueType.objects.all().order_by('title')
    try:page=int(request.GET['page'])
    except:page=1
    data = ds_pagination(venuetype,page,'venuetype',30)
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def locality_venuetype_update(request,template='admin/portal/locality/update_venuetype.html'):
    data={}
    venuetype=None
    try:
        venuetype=VenueType.objects.get(id=int(request.REQUEST['id']))
        form=VenueTypeForm(instance=venuetype)
    except:form=VenueTypeForm()
    if request.method=='POST':
        if venuetype:form=VenueTypeForm(request.POST,instance=venuetype)
        else:form=VenueTypeForm(request.POST)
        if form.is_valid():
            vtype=form.save(commit=False)
            if venuetype:vtype.slug = getUniqueValue(VenueType,slugify(form.cleaned_data.get('slug')),instance_pk=venuetype.id)
            else:vtype.slug = getUniqueValue(VenueType,slugify(form.cleaned_data.get('slug')))
            vtype.save() 
            form=VenueTypeForm()
            data = {'form':form,'venuetype':venuetype}
            append_data={'cat':vtype,'edit_url':reverse('admin_portal_locality_venuetype_update')}
            return success_response_to_save_locality(append_data,data,template,LOCALITY_MSG,'T')
        else:
            data = {'form':form,'venuetype':venuetype}
            return error_response(data,template,LOCALITY_MSG)
    else:
        data = {'form':form,'venuetype':venuetype}
        return render_to_response (template, data, context_instance=RequestContext(request))
    
@admin_required
def locality_venuetype_delete(request):
    data=response_delete_locality(request,VenueType,LOCALITY_MSG,'T')
    return HttpResponse(simplejson.dumps(data))

###############################################VENUE##########################################################

@admin_required
def locality_venue(request,template='admin/portal/locality/venue.html'):
    venues=Address.objects.all().order_by('venue')
    try:page=int(request.GET['page'])
    except:page=1
    data = ds_pagination(venues,page,'venues',20)
    data['url'] = reverse('admin_portal_locality_venue')
    try:data['msg']=LOCALITY_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=get_msg_class_name(request.REQUEST['mtype'])
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def locality_venue_update(request,id=None,template='admin/portal/locality/update_venue.html'):
    data={}
    venue=None
    try:data['page']=page=str(request.GET['page'])
    except:data['page']=page=str(1)
    if id:
        data['venue']=venue=Address.objects.get(id=id)
        form=VenueForm(instance=venue)
    else:form=VenueForm()
    if request.method=='POST':
        if venue:form=VenueForm(request.POST,instance=venue)
        else:form=VenueForm(request.POST)
        if form.is_valid():
            venue=form.save(commit=False)
            try:
                venue.lat, venue.lon, venue.zoom = get_lat_lng(request.POST['lat_lng'])
                try:venue.zoom = int(request.POST['zoom'])
                except:pass
            except:venue.lat, venue.lon, venue.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            venue.created_by=venue.modified_by=request.user
            if not venue.seo_title:venue.seo_title=venue.venue
            if not venue.seo_description:venue.seo_description=venue.description[:400]
            venue.save()
            try:
                if request.POST['add_venue']:
                    try:photo_id=request.POST['photo_list'].split(',')
                    except:photo_id=request.POST['photo_list']
                    photo = VenuePhoto.objects.filter(id__in=photo_id)
                    photo.update(venue=venue)
                    photo.update(title=venue.venue)
            except:pass
            try:
                flag=request.POST['addanother']
                return HttpResponseRedirect(reverse('admin_portal_locality_venue_add')+"?page="+page+"&mtype=s&msg=VUS")
            except:return HttpResponseRedirect(reverse('admin_portal_locality_venue')+"?page="+page+"&mtype=s&msg=VUS")
    data['form']=form
    try:data['msg']=LOCALITY_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def locality_venue_delete(request):
    data=response_delete_locality(request,Address,LOCALITY_MSG,'V')
    return HttpResponse(simplejson.dumps(data))

#############################################SEO##########################################################

@admin_required
def locality_venue_seo(request, template='admin/portal/locality/seo.html'):
    venues=Address.objects.all().order_by('venue')
    try:page=int(request.GET['page'])
    except:page=1
    data = ds_pagination(venues,page,'venues',20)
    data['url'] = reverse('admin_portal_locality_venue_seo')
    try:data['msg']=LOCALITY_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def locality_venue_seo_update(request, template='admin/portal/locality/update_seo.html'):
    data={}
    venue=Address.objects.get(id=int(request.REQUEST['id']))
    form=VenueSeoForm(instance=venue)
    if request.method=='POST':
        form=VenueSeoForm(request.POST,instance=venue)
        if form.is_valid():
            seo_form=form.save()
            data={'status':1,'msg':str(LOCALITY_MSG['VSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data = {'form':form,'seo':venue}
            return error_response(data,template,LOCALITY_MSG)
    data = {'form':form,'seo':venue}
    return render_to_response (template, data, context_instance=RequestContext(request))
    
@admin_required
def locality_auto_suggest_pin(request):
    data = Zipcode.objects.all().distinct()
    data=data.filter(zip__icontains=request.GET['input'])[:10]
    response_dict = {}
    child_dict = []
    response_dict.update({'results':child_dict})
    for tag in data :
        buf={}
        buf.update({'id':tag.id})
        buf.update({'value':tag.zip})
        buf.update({'info':''})
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

######################### Gallery Upload  ######################################
from common.fileupload import upload_photos,delete_photos

@admin_required
def locality_ajax_upload_photos(request):  
    try:venue = Address.objects.get(id=request.GET['id'])
    except:venue=None
    return upload_photos(request,VenuePhoto,venue,'venue')

@admin_required
def locality_ajax_delete_photos(request,pk):
    return delete_photos(request,VenuePhoto,pk)