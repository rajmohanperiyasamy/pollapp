import urllib2
from xml.etree import ElementTree 
# Django Libs 
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
#Application Libs and Common Methods
from common.templatetags.ds_utils import get_msg_class_name
from hotels.forms import ApiSettingsForm
from common.static_msg import API_MSG
from common.utils import get_global_settings
from common.forms import SEOForm 
from common.models import ModuleNames

from hotels.models import ApiSettings
from usermgmt.decorators import admin_required

@admin_required    
def hotels_configuration(request,template='admin/portal/api/hotels-config.html'):
    ''' method for displaying the hotel config information '''
    global_settings = get_global_settings()
    try:api_settings_obj = ApiSettings.objects.all()[:1][0]
    except:api_settings_obj=False
    
    if api_settings_obj:form = ApiSettingsForm(initial={'city': global_settings.city},instance=api_settings_obj)
    else:form = ApiSettingsForm(initial={'city': global_settings.city})
    
    try:seo = ModuleNames.get_module_seo(name='hotels')
    except:seo=None
    
    data={'api_settings_obj':api_settings_obj,'form':form,'seo':seo}
    return render_to_response (template, data, context_instance=RequestContext(request))   
    
@admin_required    
def update_hotel_api_settings(request,template='admin/portal/api/hotels-api-settings.html'):
    ''' method for saving hotel api settings info'''
    try:api_settings_obj = ApiSettings.objects.all()[:1][0]
    except:api_settings_obj=False
    
    if api_settings_obj:form = ApiSettingsForm(request.POST,instance=api_settings_obj)
    else:form = ApiSettingsForm(request.POST)
    
    if form.is_valid():
        api_settings = form.save(commit=False)
        api_settings.option = request.POST['option']
        api_settings.save()
    else:
        form = form
    
    seoform = SEOForm(request.POST)
    try:seo = ModuleNames.get_module_seo(name='hotels')
    except:seo = ModuleNames(name='hotels')
    if seoform.is_valid():
        title = seoform.cleaned_data.get('meta_title')
        description = seoform.cleaned_data.get('meta_description')
        seo.seo_title = title
        seo.seo_description = description
        seo.modified_by = request.user
        seo.save() 
            
    data={'api_settings_obj':api_settings_obj,'form':form,'seo':seo,'seoform':seoform}  
    html=render_to_string(template,data,context_instance=RequestContext(request))
    return_data = {'html':html,'msg':str(API_MSG['HAUS']),'mtype':get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(return_data))
 
@admin_required     
def validate_hotels_api(request):
    try:
        api_key=request.POST['api_key']
        customer_id=request.POST['customer_id']
        city=request.POST['city']
        
        url = 'http://api.ean.com/ean-services/rs/hotel/v3/list?type=xml&apiKey=%s&cid=%s&locale=en_US&city=%s&minorRev=12'%(api_key,customer_id,urllib2.quote(city))
        request = urllib2.Request(url, headers={"Accept" : "application/xml"})
        xml = urllib2.urlopen(request)
        tree = ElementTree.parse(xml)
        rootElem = tree.getroot()
       
        try:
            hotel_list = rootElem.find('HotelList').findall("HotelSummary")
            return HttpResponse('1')
        except:
            hotel_list = rootElem.find('EanWsError')
            return HttpResponse('0')
    except:
        return HttpResponse('0')
