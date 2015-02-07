from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.vary import vary_on_headers
from django.utils import simplejson

from locality.models import * 
from django.conf import settings
from common.utils import get_global_settings

def getXmlLocation(request):
    try:
        locality = Locality.objects.get(id=int(request.GET['locality']))
        lat = locality.latitude
        lng = locality.longitude
        zoom = locality.zoom
    except:
        try:
            locality = Locality.objects.get(name=request.GET['locality'])
            lat = locality.latitude
            lng = locality.longitude
            zoom = locality.zoom
        except:
            global_settings = get_global_settings()
            lat=global_settings.google_map_lat
            lng=global_settings.google_map_lon
            zoom=global_settings.google_map_zoom
    try:
        zipcode=""
        for zip in locality.zipcodes.all():
            zipcode+="<zipcode id='"+str(zip.id)+"' zip='"+str(zip.zip)+"'></zipcode>"
    except:zipcode=""
    xmldata="""<markers>
    <marker lat='"""+str(lat)+"""' lng='"""+str(lng)+"""' zoom='"""+str(zoom)+"""' address='fdsf gfgfggfgf' type='green' name='frazertown'/>
    """+zipcode+"""</markers>"""
    return HttpResponse(xmldata, mimetype='application/xml')

def auto_suggest_pin(request):
    try:
        data = Locality.objects.get(id=int(request.GET['lid']))
        data=data.zipcodes.all()
        data=data.filter(zip__icontains=request.GET['input'])
    except:
        data = Zipcode.objects.all()
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

def suggest_pin(request):
    try:data = Zipcode.objects.filter(zip__icontains=request.GET['term'])[:10]
    except:data = Zipcode.objects.all()[:10]
    child_dict = []
    for zip in data :
        buf={'label':zip.zip,'id':zip.id,'value':zip.zip}
        child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), mimetype='application/javascript')