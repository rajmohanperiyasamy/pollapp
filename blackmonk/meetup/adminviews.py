#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.template.loader import render_to_string
#Library
from common.static_msg import MEETUP_MSG
from common.admin_utils import response_delete_category,response_to_save_settings
from common.forms import SEOForm 
from common.models import ModuleNames 
from common.templatetags.ds_utils import get_msg_class_name
from usermgmt.decorators import admin_required

from meetup.models import MeetupSettings
from meetup.forms import MeetupSettingsForm
from meetup.utils import get_meetup_validate

"""
#####################################################################################################################
##############################################        Meetup        #################################################
#####################################################################################################################
"""
@admin_required
def meetup_settings(request, template='admin/portal/meetup/settings.html'):
     meetup=None
     try:
         meetup = MeetupSettings.objects.all()[0]
         meetup_form=MeetupSettingsForm(instance=meetup)
     except:meetup_form=MeetupSettingsForm()
     try:seo = ModuleNames.get_module_seo(name='meetup')
     except:seo = ModuleNames(name='meetup')
     if request.method=='POST':
         if meetup:meetup_form=MeetupSettingsForm(request.POST,instance=meetup)
         else:meetup_form=MeetupSettingsForm(request.POST)
         seo_form = SEOForm(request.POST)
         ############################################
         if meetup_form.is_valid() and seo_form.is_valid():
             ############################################
             meetups=meetup_form.save(commit=False)
             meetups.status='upcoming'
             meetups.save()
             
             seo.seo_title = seo_form.cleaned_data.get('meta_title')
             seo.seo_description = seo_form.cleaned_data.get('meta_description')
             seo.modified_by = request.user
             seo.save()
             data={'seo':seo,'seo_form':seo_form,'meetup_form':meetup_form}
             return response_to_save_settings(request,True,data,'admin/portal/meetup/include_settings.html',MEETUP_MSG)
         else:
             data={'seo':seo,'seo_form':seo_form,'meetup_form':meetup_form}
             return response_to_save_settings(request,False,data,'admin/portal/meetup/include_settings.html',MEETUP_MSG)
     else:
         data={'seo':seo,'meetup_form':meetup_form}
         return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def validate_meetup_api(request):
    try:
        api_key=request.POST['api_key']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        
        zip=request.POST.get('zip',False)
        lat=request.POST.get('lat',False)
        lon=request.POST.get('lon',False)
        
        url="https://api.meetup.com/2/open_events/?sign=true&format=xml&status=upcoming&city=%s&country=%s&state=%s&key=%s"%(city,country,state,api_key)
        if zip:url=url+'&zip=%s'%(zip)
        if lat and lon:url=url+'&lon=%s&lat=%s'%(lon,lat)
        
        meetups = get_meetup_validate(url)
        if meetups:return HttpResponse('1')
        else:return HttpResponse('0')
    except:
        import sys
        print sys.exc_info()
        return HttpResponse('0')

