import suds
from suds.client import Client

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson

from common.templatetags.ds_utils import get_msg_class_name
from common.static_msg import API_MSG
from common.forms import SEOForm 
from common.models import ModuleNames

from flowers.models import FlowerApiSettings,Category
from flowers.forms import FlowerApiSettingsForm
from usermgmt.decorators import admin_required


@admin_required  
def flower_configuration(request,template='admin/portal/api/flower-config.html'):
    ''' method for displaying the flower config information '''
    data={}
    try:flower_api_obj = FlowerApiSettings.objects.all()[:1][0]
    except:flower_api_obj=False
    if flower_api_obj:form=FlowerApiSettingsForm(instance=flower_api_obj)
    else:form=FlowerApiSettingsForm()
    try:seo = ModuleNames.get_module_seo(name='flowers')
    except:seo=None
    data={'flower_api_obj':flower_api_obj,'form':form,'seo':seo}  
    return render_to_response (template, data, context_instance=RequestContext(request))   
    
@admin_required    
def update_flower_api_settings(request,template='admin/portal/api/flower-api-settings.html'): 
    ''' updating weather api settings '''
    try:flower_api_obj = FlowerApiSettings.objects.all()[:1][0]
    except:flower_api_obj=False
    
    if flower_api_obj:form = FlowerApiSettingsForm(request.POST,instance=flower_api_obj)
    else:form = FlowerApiSettingsForm(request.POST)
    
    if form.is_valid():form.save()
    else:form = form
   
    seoform = SEOForm(request.POST)
    try:seo = ModuleNames.get_module_seo(name='flowers')
    except:seo = ModuleNames(name='flowers')
    if seoform.is_valid():
        title = seoform.cleaned_data.get('meta_title')
        description = seoform.cleaned_data.get('meta_description')
        seo.seo_title = title
        seo.seo_description = description
        seo.modified_by = request.user
        seo.save() 
   
    data={'flower_api_obj':flower_api_obj,'form':form,'seo':seo,'seoform':seoform}  
    html=render_to_string(template,data,context_instance=RequestContext(request))
    return_data = {'html':html,'msg':str(API_MSG['FAUS']),'mtype':get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(return_data))   

def validate_flover_api(request):
    try:
        api_key=request.POST['api_key']
        api_password=request.POST['api_password']
        api_settings = FlowerApiSettings.objects.all()[:1][0]
        furl="https://www.floristone.com/webservices4/flowershop.cfc?wsdl"
        client = Client(furl)
        categories = Category.objects.filter(parent__isnull=False).order_by('id')[0]
        result = client.service.getProducts(str(api_key), str(api_password), str(categories.code.strip()), "100", "1")
        if result.errors:return HttpResponse('0')
        else:return HttpResponse('1')
    except:
        return HttpResponse('0') 

