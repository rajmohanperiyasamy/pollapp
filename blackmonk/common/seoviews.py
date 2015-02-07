#Python Libs

#Django Libs and Methods
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson

#Application Libs and Common Methods
from common.templatetags.ds_utils import get_msg_class_name
from common.static_msg import SEO_SETTINGS_MSG
from common.getunique import getUniqueValue
from usermgmt.decorators import admin_required

#Module Files(models,forms etc...)
from common.models import SeoSettings, MiscAttribute

SEO_FORMAT_ORDER = {'Site Title':'T','Site Name':'N','Domain Name':'D','Module Title':'T', 'Module Name':'O', 'Listing Title':'T', 'Category Name':'C', 'Item Title':'T'}

############################### ADMIN SEO CONFIGURATION ##########################################################

def __update_seo_format_order(titles,code,user):
    
    order = ''
    formated_title = ''
    title=''
    i=1
    for title in titles:
        try:
            order += SEO_FORMAT_ORDER[title]
            if i != len(titles):
                title += ','
            formated_title += title 
            i=i+1
        except:pass    
    
    try:
        seo_settings_obj = SeoSettings.objects.get(code = code)
    except:
        seo_settings_obj = SeoSettings(code = code) 
        
    seo_settings_obj.created_by = user
    seo_settings_obj.order = order
    seo_settings_obj.title = formated_title
    seo_settings_obj.save()


def __update_seo_varification(key,name,value):
    try:google_webm_tag = MiscAttribute.objects.get(attr_key=key)
    except:google_webm_tag = MiscAttribute(attr_key=key)
    google_webm_tag.attr_name = name
    google_webm_tag.attr_value = value
    google_webm_tag.save()
    

@admin_required
def seo_overview(request, template='admin/seo/manage-seo.html'):
    ''' displays seo settings page '''
    data={}
    
    try:data['home_title'] = SeoSettings.objects.get(code='HT')
    except:data['home_title'] = False
    try:data['module_title'] = SeoSettings.objects.get(code='MT')
    except:data['module_title'] = False
    try:data['listing_title'] = SeoSettings.objects.get(code='LT')
    except:data['listing_title'] = False
    try:data['detail_title'] = SeoSettings.objects.get(code='DT')
    except:data['detail_title'] = False
    
    try:data['google_webm_tag'] = MiscAttribute.objects.get(attr_key='GOOGLE_WEBM_TAG')
    except:data['google_webm_tag'] = False
    try:data['robot_txt'] = MiscAttribute.objects.get(attr_key='ROBOT_TXT')
    except:data['robot_txt'] = False
    try:data['bing_webm_tag'] = MiscAttribute.objects.get(attr_key='BING_WEBM_TAG')
    except:data['bing_webm_tag'] = False
    
    return render_to_response (template, data, context_instance=RequestContext(request))





@admin_required
def update_seo_settings(request):
    
    try:
        __update_seo_format_order(request.REQUEST['home_title'].split(','), 'HT', request.user)   
        __update_seo_format_order(request.REQUEST['module_title'].split(','), 'MT', request.user)   
        __update_seo_format_order(request.REQUEST['listing_title'].split(','), 'LT', request.user)   
        __update_seo_format_order(request.REQUEST['detail_title'].split(','), 'DT', request.user)   
        status = True
    except:
        status = False
    
    __update_seo_varification('GOOGLE_WEBM_TAG','Google Webmaster Meta Tag',request.POST['google_webm_tag'])
    __update_seo_varification('BING_WEBM_TAG','Bing Webmaster Meta Tag',request.POST['bing_webm_tag'])
    __update_seo_varification('ROBOT_TXT','Robot Txt',request.POST['robot_txt'])
    
    
    
    
    return_data = {'status':status,'msg':str(SEO_SETTINGS_MSG['SFUS']),'mtype':get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(return_data))