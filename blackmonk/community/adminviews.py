#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count

#Library
from common.static_msg import ADVICE_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category
from common.admin_utils import response_to_save_settings,save_emailsettings,get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.models import ModuleNames,ApprovalSettings
from common.forms import ApprovalSettingForm,SEOForm
from usermgmt.decorators import admin_required

from community.models import Topic,Entry
from community.forms import CommunityTopicForm,CommunityTopicSeoForm


"""
#####################################################################################################################
##############################################        COMMUNITY        #################################################
#####################################################################################################################
"""
@admin_required
def community_settings(request, template='admin/portal/advice/settings.html'):
    approval=None
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    category=Topic.objects.all().count()
    no_answers = Entry.objects.filter(entry_type="A").count()
    entry_state = Entry.objects.filter(entry_type="Q").values('status').annotate(s_count=Count('status'))
    questions = Entry.objects.filter(entry_type="Q",status="P").count()
    
    for st in entry_state:
        STATE[st['status']]+=st['s_count']
        
    data={
          'questions':questions,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'category':category,
          'no_answers':no_answers,
    }
    
    try:
        approval = ApprovalSettings.objects.get(name='community')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:seo = ModuleNames.get_module_seo(name='community')
    except:seo = ModuleNames(name='community')
    if request.method=='POST':
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        seo_form = SEOForm(request.POST)
        if approval_form.is_valid() and seo_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='community'
            approvals.modified_by=request.user
            approvals.save()
            
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            save_emailsettings(request,'community')
            extra_data={'approval_form':approval_form,'emailsettings':get_emailsettings('community'),'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/advice/include_settings.html',ADVICE_MSG)
        else:
            extra_data={'approval_form':approval_form,'emailsettings':get_emailsettings('community'),'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/advice/include_settings.html',ADVICE_MSG)
    else:
        extra_data={'approval_form':approval_form,'emailsettings':get_emailsettings('community'),'seo':seo}
        data.update(extra_data)
        return render_to_response (template, data, context_instance=RequestContext(request))


################################################## CATEGORY #########################################
@admin_required
def advice_category(request, template='admin/portal/advice/category.html'):
    topics=Topic.objects.order_by('name')
    data={'topics':topics}
    try:data['msg']=ADVICE_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def advice_category_update(request,template='admin/portal/advice/update_category.html'):
    data={}
    cat=None
    try:
        cat = Topic.objects.get(id=request.REQUEST['id'])
        form = CommunityTopicForm(instance=cat)
    except:form = CommunityTopicForm()
    if request.method=='POST':
        if cat:form = CommunityTopicForm(request.POST,instance=cat)
        else:form = CommunityTopicForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if cat:
                if category.slug:category.slug = getUniqueValue(Topic,slugify(form.cleaned_data.get('slug')),instance_pk=category.id)
                else:category.slug = getUniqueValue(Topic,slugify(form.cleaned_data.get('name')),instance_pk=category.id)
            else:
                if category.slug:category.slug = getUniqueValue(Topic,slugify(form.cleaned_data.get('slug')))
                else:category.slug = getUniqueValue(Topic,slugify(form.cleaned_data.get('name')))
            category.save()
            form=CommunityTopicForm()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('admin_portal_advice_category_update')}
            return success_response_to_save_category(append_data,data,template,ADVICE_MSG)
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,ADVICE_MSG)
    else:
        data = {'form':form,'cat':cat}
        return render_to_response(template,data,context_instance=RequestContext(request))
        
@admin_required
def advice_category_delete(request):
    data=response_delete_category(request,Topic,ADVICE_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def advice_seo_category_update(request, template='admin/portal/advice/update_category_seo.html'):
    try:seo = Topic.objects.get(id=int(request.REQUEST['id']))
    except:return HttpResponse(str(ADVICE_MSG['CNF']))
    form=CommunityTopicSeoForm(instance=seo)
    if request.method=='POST':
        form = CommunityTopicSeoForm(request.POST,instance=seo)
        if form.is_valid():
            seo=form.save(commit=False)
            try:seo.slug = getUniqueValue(Topic,slugify(request.POST['slug']),instance_pk=seo.id)
            except:seo.slug = getUniqueValue(Topic,slugify(seo.name),instance_pk=seo.id)
            seo.save()
            data={'status':1,'msg':str(ADVICE_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data = {'form':form,'seo':seo}
            return error_response(data,template,ADVICE_MSG)
    data={'seo':seo,'form':form}
    return render_to_response (template, data, context_instance=RequestContext(request))



