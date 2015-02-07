import urllib2
from xml.etree import ElementTree 
#Django
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

#Library
from common.static_msg import JOBS_MSG
from common.admin_utils import response_to_save_settings
from common.templatetags.ds_utils import get_msg_class_name
from common.forms import SEOForm
from common.models import ModuleNames
from usermgmt.decorators import admin_required

from jobs.forms import JobSettingsForm
from jobs.models import JobSettings,JobCategory

@admin_required
def jobs_settings(request, template='admin/portal/jobs/settings.html'):
    try:
        jobs=JobSettings.objects.all()[:1][0]
        form=JobSettingsForm(instance=jobs)
    except:
        jobs = False
        form=JobSettingsForm()
    
    try:seo = ModuleNames.get_module_seo(name='jobs')
    except:seo = ModuleNames(name='jobs')        
    if request.method=='POST':
        if jobs:form=JobSettingsForm(request.POST,instance=jobs)
        else:form=JobSettingsForm(request.POST)
        seo_form = SEOForm(request.POST)
        if seo_form.is_valid() and form.is_valid(): 
            form.save()
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            data = {'seo':seo,'seo_form':seo_form,'form':form}
            return response_to_save_settings(request,True,data,'admin/portal/jobs/include_settings.html',JOBS_MSG)
        else:
            data = {'seo':seo,'seo_form':seo_form,'form':form}
            return response_to_save_settings(request,False,data,'admin/portal/jobs/include_settings.html',JOBS_MSG)
    data = {'seo':seo,'form':form }
    return render_to_response (template, data, context_instance=RequestContext(request))

def get_api_url(request,cat,page):
    url = request.POST['jurl']
    url = '%sq-%s/pn=%s'%(url,cat,page)
    location=request.POST.get('location',False)
    if location:url = '/%s/l-%s'%(url,location)
    url = '%s?pshid=%s&ssty=%s&cflg=%s&jbd=%s'%(url,request.POST['pshid'],request.POST['ssty'],request.POST['cflg'],request.POST['jbd'])    
    return url

@admin_required
def validate_jobs_api(request):
    try:
        try:category = JobCategory.objects.all()[0].key
        except:category = 'Accounting Finance'
        url = get_api_url(request,category,1)
        request = urllib2.Request(url, headers={"Accept" : "application/xml"})
        xml = urllib2.urlopen(request)
        tree = ElementTree.parse(xml)
        rootElem = tree.getroot()
        try:job_list = rootElem.find('rs').findall("r")
        except:job_list = rootElem.find('error').attrib.get('type')
        if job_list == 'invalidparam':
            return HttpResponse('0')
        else:
            return HttpResponse('1')
    except:return HttpResponse('0')



