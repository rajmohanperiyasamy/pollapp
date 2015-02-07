#Django
from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.db.models import Count
from django.utils import simplejson

from common.static_msg import SWEEPSTAKES_MSG
from common.admin_utils import response_to_save_settings,success_response_to_save_qanda,response_delete_qanda,error_response
from common.models import ModuleNames
from common.forms import SEOForm
from usermgmt.decorators import admin_required

from sweepstakes.models import Sweepstakes,SweepstakesQandA,SweepstakesSettings
from sweepstakes.forms import SweepstakesQandAForm


"""
#####################################################################################################################
##############################################        Sweepstakes       #############################################
#####################################################################################################################
"""
@admin_required
def sweepstakes_settings(request, template='admin/portal/sweepstakes/settings.html'):
    sweepstakes=0
    STATE={'E':0,'P':0,'N':0,'B':0}
    sweepstakes_state = Sweepstakes.objects.values('status').annotate(s_count=Count('status'))

    for st in sweepstakes_state:
        STATE[st['status']]+=st['s_count']
        sweepstakes=sweepstakes+1
    data={'sweepstakes':sweepstakes,'published':STATE['P'],'pending':STATE['N'],'blocked':STATE['B'],'expired':STATE['E']}
    try:seo = ModuleNames.get_module_seo(name='sweepstakes')
    except:seo = ModuleNames(name='sweepstakes')
    try:settings=SweepstakesSettings.objects.all()[0]
    except:settings=None
   
    if request.method=='POST':
        seo_form = SEOForm(request.POST)
        if seo_form.is_valid():
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            if not settings:settings=SweepstakesSettings()
            settings.email=request.POST['email']
            settings.save()
            extra_data={'seo':seo,'seo_form':seo_form,'settings':settings}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/sweepstakes/include_settings.html',SWEEPSTAKES_MSG)
        else:
            extra_data={'seo':seo,'seo_form':seo_form,'settings':settings}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/sweepstakes/include_settings.html',SWEEPSTAKES_MSG)
    else:
        extra_data={'seo':seo,'settings':settings}
        data.update(extra_data)
        return render_to_response (template, data, context_instance=RequestContext(request))

def sweepstakes_qanda(request,template='admin/portal/sweepstakes/qanda.html'):
    data={}
    data['qandas']=SweepstakesQandA.objects.all().order_by('position')
    try:data['msg']=SWEEPSTAKES_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

def sweepstakes_qanda_update(request,template='admin/portal/sweepstakes/update_qanda.html'):
    data={}
    qanda=None
    try:
        qanda = SweepstakesQandA.objects.get(id=request.REQUEST['id'])
        form = SweepstakesQandAForm(instance=qanda)
    except:form = SweepstakesQandAForm()
    if request.method=='POST':
        if qanda:form = SweepstakesQandAForm(request.POST,instance=qanda)
        else:form = SweepstakesQandAForm(request.POST)
        if form.is_valid():
            qanda = form.save(commit=False)
            qanda.save()
            form=SweepstakesQandAForm()
            data = {'form':form,'qanda':qanda,'new_qanda':True}
            append_data={'qanda':qanda,'edit_url':reverse('admin_portal_sweepstakes_qanda_update')}
            return success_response_to_save_qanda(append_data,data,template,SWEEPSTAKES_MSG)
        else:
            data = {'form':form,'qanda':qanda}
            return error_response(data,template,SWEEPSTAKES_MSG)
    else:
        data = {'form':form,'qanda':qanda}
        return render_to_response(template,data,context_instance=RequestContext(request))
            
def sweepstakes_qanda_delete(request):
    data=response_delete_qanda(request,SweepstakesQandA,SWEEPSTAKES_MSG)
    return HttpResponse(simplejson.dumps(data))






