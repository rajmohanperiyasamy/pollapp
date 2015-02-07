# Django Libs 
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
#Application Libs and Common Methods
from common.templatetags.ds_utils import get_msg_class_name
from common.static_msg import API_MSG
from common.models import AvailableApps
#Module Files(models,forms etc...)
from common.models import WeatherApiSettings
from usermgmt.decorators import admin_required


@admin_required
def api_overviews(request,template='admin/api_dashboard.html'):
    apps=AvailableApps.objects.filter(status='A',type='A').order_by('name')
    data={'apps':apps}
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required  
def weather_configuration(request,template='admin/portal/api/weather-config.html'):
    ''' method for displaying the weather config information '''
    data={}
    try:wx_api_obj = WeatherApiSettings.objects.all()[:1][0]
    except:wx_api_obj=False
    
    data={'wx_api_obj':wx_api_obj}  
    return render_to_response (template, data, context_instance=RequestContext(request))   
    
@admin_required    
def update_weather_api_settings(request,template='admin/portal/api/weather-api-settings.html'): 
    ''' updating weather api settings '''
    try:wx_api_obj = WeatherApiSettings.objects.all()[:1][0]
    except:wx_api_obj=WeatherApiSettings()
    
    wx_api_obj.option = request.POST['option']
    wx_api_obj.weather_xml = request.POST['weather_url']
    wx_api_obj.weather_unit = request.POST['weather_unit']
    wx_api_obj.save()
    
    data={'wx_api_obj':wx_api_obj}  
    html=render_to_string(template,data,context_instance=RequestContext(request))
    return_data = {'html':html,'msg':str(API_MSG['WAUS']),'mtype':get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(return_data))   
     
  
       
