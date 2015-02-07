from PIL import Image
from xml.dom import minidom
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.template import Context
from django.template import RequestContext
from django import forms
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.core.cache import cache
from django.template.loader import render_to_string
from django.conf import settings

from locality.models import *
from locality.forms import *

from common.getunique import getUniqueValue
from common.imagehandling import cropImage, imageThumbnail
from common.utils import ds_pagination,get_global_settings,get_lat_lng  
from common.staff_messages import LOCALITY_MSG
from common.templatetags.ds_utils import get_msg_class_name
from common.admin_utils import error_response
from common.models import Address


@staff_member_required
def manage_location(request):
    (localityall) = Locality.objects.all().order_by('name')
    data = {
            'localityall': localityall,
            }
    try:
        data['message'] = request.GET['m']
    except:pass
    return render_to_response('locality/staff/managelocations.html', data,context_instance=RequestContext(request))

@staff_member_required
def add_location(request):
    if request.method != 'POST':
        form = LocationForm()
        data = {'form': form,}
        try:
            data['message'] = request.GET['m']
        except:pass
        return render_to_response('locality/staff/addlocation.html', data,context_instance=RequestContext(request))
    else:
        form = LocationForm(request.POST)
        if form.is_valid():
            loca = form.save(commit=False)
            loca.latitude, loca.longitude, loca.zoom = get_lat_lng(request.POST['lat_lng'])
            try:loca.zoom = int(request.POST['zoom'])
            except:pass
            loca.save()
            form.save_m2m()
            return HttpResponseRedirect('/staff/locality/add/?m=new location added successfully')
        else:
            data = {
                    'form': form,
                    }
            return render_to_response('locality/staff/addlocation.html', data,context_instance=RequestContext(request))
        return HttpResponseRedirect('/staff/locality/')
add_location = permission_required('locality.add_locality')(add_location)

@staff_member_required
def delete_location(request):
    try:
        sloca = Locality.objects.get(id=request.GET['lid'])
        url = "/staff/locality/?m='%s' location deleted successfully"%(sloca.name)
        sloca.delete()
        return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect('/staff/locality/')
delete_location = permission_required('locality.delete_locality')(delete_location)

def edit_location(request):
    try:
        locality = Locality.objects.get(id=request.GET['lid'])
    except:
        return HttpResponseRedirect('/staff/locality/')
    if request.method != 'POST':
        form = LocationForm(instance=locality)
        data = {
            'locality': locality,
            'form': form,
        }
        try:data['message'] = request.GET['m']
        except:pass
        return render_to_response('locality/staff/editlocation.html', data,context_instance=RequestContext(request))
    else:
        form = LocationForm(request.POST, instance=locality)
        if form.is_valid():
            loca = form.save(commit=False)
            loca.latitude, loca.longitude, loca.zoom = get_lat_lng(request.POST['lat_lng'])
            try:loca.zoom = int(request.POST['zoom'])
            except:pass
            loca.save()
            form.save_m2m()
            return HttpResponseRedirect('/staff/locality/?m=update location successfully')
        else:
            data = {
                    'form': form,
                    'locality': locality,
                    }
            return render_to_response('locality/staff/editlocation.html', data,context_instance=RequestContext(request))
        return HttpResponseRedirect('/staff/locality/')
edit_location = permission_required('locality.change_locality')(edit_location)

def get_locality(request):
    from django.utils import simplejson
    ajax_zip = request.GET['ajax_zip']
    try:
        location = Locality.objects.get(pin=ajax_zip)
        
        data = {
            'loc_id': location.id,
            'loc_name':location.name,
        }
    except:
        data = {'notfound':'true'}
    return HttpResponse(simplejson.dumps(data))

################### Manage Zip Code ####################

def manage_zip(request,template='locality/staff/manage-zip.html'):
    (zipall) = Zipcode.objects.all().order_by('zip')
    data = {
            'zipall': zipall,
            }
    try:
        data['message'] = request.GET['m']
    except:pass
    return render_to_response(template, data,context_instance=RequestContext(request))

@staff_member_required
def add_zip(request,template='locality/staff/add-zip.html'):
    data ={}
    if request.method != 'POST':
        form = ZipForm()
        data['form']=form 
        try:
            data['message'] = request.GET['m']
        except:pass
    else:
        form = ZipForm(request.POST)
        if form.is_valid():
            loca = form.save(commit=False)
            loca.latitude, loca.longitude, loca.zoom = get_lat_lng(request.POST['lat_lng'])
            try:loca.zoom = int(request.POST['zoom'])
            except:pass
            loca.save()
            return HttpResponseRedirect('/staff/locality/addzip/?m=new zip code added successfully')
        else:
            data['form']=form 
    return render_to_response(template, data,context_instance=RequestContext(request))
    
@staff_member_required
def delete_zip(request):
    try:
        zip = Zipcode.objects.get(id=request.GET['zid'])
        url = "/staff/locality/zip/?m='%s' zip code deleted successfully"%(zip.zip)
        zip.delete()
        return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect('/staff/locality/zip/')

@staff_member_required       
def common_ajax_add_venue(request,template='locality/staff/ajax-add-venue.html'):
    global_settings = get_global_settings()
    data={}
    try:venue=venue_obj=Address.objects.get(id=int(request.GET['id']))
    except:venue=venue_obj=False
    if request.method=='POST':
        if venue:form=VenueForm(request.POST,instance=venue)
        else:form=VenueForm(request.POST)
        if form.is_valid():
            venue=form.save(commit=False)
            try:
                venue.lat, venue.lon, venue.zoom = get_lat_lng(request.POST['lat_lng'])
                try:venue.zoom = int(request.POST['map_zoom'])
                except:pass
            except:venue.lat, venue.lon, venue.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            venue.created_by=venue.modified_by=request.user
            if not venue.seo_title:venue.seo_title=venue.venue
            if not venue.seo_description:venue.seo_description=venue.description[:400]
            venue.save()
            template_name='attraction/staff/ajax_address.html'
            return_data = {}
            return_data['venue'] = venue
            html=render_to_string(template_name,return_data, context_instance=RequestContext(request))
            address=str(venue.venue)+','+str(venue.address1)+','+str(venue.zip)
            if venue_obj:
                send_data={'status':1,'msg':str(LOCALITY_MSG['SUV']),'mtype':get_msg_class_name('s'),'address':address,'id':venue.id ,'html':html}
            else:
                send_data={'status':1,'msg':str(LOCALITY_MSG['SAV']),'mtype':get_msg_class_name('s'),'address':address,'id':venue.id ,'html':html}
            return HttpResponse(simplejson.dumps(send_data))
        else:
            data['form']=form  
            data['venue']=venue
            return error_response(data,template,LOCALITY_MSG)  
    else:
        if venue:form=VenueForm(instance=venue)
        else:form=VenueForm()
        data['venue']=venue
        data['form']=form  
        return render_to_response(template ,data,context_instance=RequestContext(request))

@staff_member_required    
def common_auto_suggest_venue(request):
    try:data = Address.objects.filter(venue__icontains=request.GET['term'])[:10]
    except:data = Address.objects.all()[:10]
    main=[]
    for ve in data:
       if ve.zip:
           values=','.join([str(ve.venue), str(ve.address1),str(ve.zip)])
       else:
            values=','.join([str(ve.venue), str(ve.address1)]) 
       b={'label':values,'id':str(ve.id),'label':values,'userid':ve.created_by.id}
       main.append(b)

    return HttpResponse(simplejson.dumps(main))

@staff_member_required    
def common_auto_suggest_zip(request):
    try:data = Zipcode.objects.filter(zip__icontains=request.GET['term'])[:10]
    except:data = Zipcode.objects.all()[:10]
    main=[]
    for ve in data:
       b={'label':ve.zip,'id':str(ve.id),'label':ve.zip}
       main.append(b)
    return HttpResponse(simplejson.dumps(main))