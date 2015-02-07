#Python

#Django
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count

#Library
from common.admin_utils import response_to_save_settings
from common.static_msg import POLLS_MSG
from common.forms import SEOForm
from common.models import ModuleNames
from usermgmt.decorators import admin_required
from polls.models import Poll

"""
#####################################################################################################################
#################################   ADMIN PORTAL POLLS        ########################################################
#####################################################################################################################
"""

@admin_required
def polls_settings(request, template='admin/portal/polls/settings.html'):
    STATE={'P':0,'N':0,'E':0,'B':0}
    polls=0
    poll_state = Poll.objects.values('status').annotate(s_count=Count('status'))
    for st in poll_state:
        STATE[st['status']]+=st['s_count']
        polls=polls+1
    
    data={ 
          'polls':polls,
          'published':STATE['P'],
          'pending':STATE['N'],
          'expired':STATE['E'],
          'blocked':STATE['B']
    }
    try:seo = ModuleNames.get_module_seo(name='polls')
    except:seo = ModuleNames(name='polls')        
    if request.method=='POST':
        seo_form = SEOForm(request.POST)
        if seo_form.is_valid(): 
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/polls/include_settings.html',POLLS_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/polls/include_settings.html',POLLS_MSG)
    data['seo'] = seo
    return render_to_response (template, data, context_instance=RequestContext(request))


