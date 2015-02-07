#Python

#Django
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.utils import simplejson
from django.contrib import messages

#Library
from common.static_msg import DEALS_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category
from common.admin_utils import response_to_save_settings,save_emailsettings,get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.forms import SEOForm
from common.models import ModuleNames
from usermgmt.decorators import admin_required

from deal.models import DealCategory,Deal,Faqs,How
from deal.forms import DealCategoryForm,DealFaqForm,DealHowForm

"""
#####################################################################################################################
#################################       ADMIN PORTAL Deals     ######################################################
#####################################################################################################################
"""
    
@admin_required
def deals_settings(request, template='admin/portal/deals/settings.html'):
    try:seo = ModuleNames.get_module_seo(name='deals')
    except:seo = ModuleNames(name='deals')
    if request.method=='POST':
        seo_form = SEOForm(request.POST)
        if seo_form.is_valid(): 
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
        save_emailsettings(request,'deals')
        data={
          'seo':seo,'seo_form':seo_form,
          'deals':Deal.objects.all().count(),
          'category':DealCategory.objects.all().count(),
          'deal_settings':True,'emailsettings':get_emailsettings('deals')
          }
        return response_to_save_settings(request,True,data,'admin/portal/deals/include_settings.html',DEALS_MSG)
    data={
          'seo':seo,
          'deals':Deal.objects.all().count(),
          'category':DealCategory.objects.all().count(),
          'deal_settings':True,'emailsettings':get_emailsettings('deals')
          }
    return render_to_response (template, data, context_instance=RequestContext(request))

################################################## CATEGORY   #########################################

@admin_required
def deals_category(request, template='admin/portal/deals/category.html'):
    cat=DealCategory.objects.order_by('name')
    data={'categoryes':cat}
    try:data['msg']=request.REQUEST['msg']
    except:pass
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def deals_category_update(request,template='admin/portal/deals/update_category.html'):
    data={}
    category=None
    try:
        category = DealCategory.objects.get(id = request.REQUEST['id'])
        form=DealCategoryForm(instance=category)
    except:form=DealCategoryForm()
    if request.POST:
        if category:form=DealCategoryForm(request.POST,instance=category)
        else: form=DealCategoryForm(request.POST)
        if form.is_valid():
            cat_form=form.save(commit=False)
            if not category:cat_form.created_by=request.user
            cat_form.modified_by=request.user
            cat_form.slug = getUniqueValue(DealCategory,slugify(cat_form.name),instance_pk=cat_form.id)
            cat_form.save()
            form=DealCategoryForm()
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_deals_category_update')}
            return success_response_to_save_category(append_data,data,template,DEALS_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data,template,DEALS_MSG)
    else:
        data = {'form':form,'cat':category}
        return render_to_response(template,data,context_instance=RequestContext(request))


@admin_required
def deals_category_delete(request):
    data=response_delete_category(request,DealCategory,DEALS_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def deals_faq(request, template='admin/portal/deals/manage_faq.html'):
    data = {}
    try:data['msg'] = DEALS_MSG[request.REQUEST['msg']]
    except:pass
    try:data['mtype'] = get_msg_class_name(request.REQUEST['mtype'])
    except:data['mtype']=None
    try:data['faqs'] = Faqs.objects.all().order_by('id')
    except:data['faqs'] = False
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def deals_add_faq(request, template='admin/portal/deals/add-faq.html'):
    data = {}
    faq=None
    try:
        faq = Faqs.objects.get(id = request.REQUEST['id'])
        form=DealFaqForm(instance=faq)
    except:form=DealFaqForm()
    if request.POST:
        if faq:form=DealFaqForm(request.POST,instance=faq)
        else: form=DealFaqForm(request.POST)
        if form.is_valid():
            faq_form=form.save(commit=False)
            faq_form.save()
            messages.success(request, str(DEALS_MSG['DFS']))
            return HttpResponseRedirect(reverse('admin_portal_deals_faq'))
        else:
            messages.error(request, str(DEALS_MSG['OOPS']))
            return HttpResponseRedirect(reverse('admin_portal_deals_faq'))
    else:
        data = {'form':form,'faq':faq}
        return render_to_response (template, data, context_instance=RequestContext(request))
    
@admin_required
def deals_faq_delete(request):
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        fq = Faqs.objects.filter(id__in=id)
        fq.delete()
        status=1
        msg=DEALS_MSG['DDS']
        mtype='s'
    except:
        status=0
        msg=DEALS_MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))   

@admin_required
def deals_how(request,template='admin/portal/deals/how.html'): 
    data = {}
    try:data['how_description'] = How.objects.get(heading = 'dcr')
    except:data['how_description'] = False
    try:data['how'] = How.objects.all().exclude(heading = 'dcr').order_by('id')
    except:data['how'] = False
    return render_to_response (template, data, context_instance=RequestContext(request))
    
@admin_required
def update_dcrptn(request, template='admin/portal/deals/add-descriptn.html'):
    data = {}
    faq=None
    id = request.REQUEST['did']
    try:
        how = How.objects.get(heading=id)
    except:
        how = False 
    if request.POST:
        if not how:
            how = How(heading=id) 
            how.save()
        how.content = request.POST['description']  
        how.save()  
        messages.success(request, str(DEALS_MSG['DUS']))
        return HttpResponseRedirect(reverse('admin_portal_deals_how'))
    else:
        data = {'how':how}
        return render_to_response (template, data, context_instance=RequestContext(request))    
    
@admin_required
def deals_how_add(request, template='admin/portal/deals/add_how.html'):
    data = {}
    how=None
    try:
        how = How.objects.get(id = request.REQUEST['id'])
        form=DealHowForm(instance=how)
    except:form=DealHowForm()
    if request.POST:
        if how:form=DealHowForm(request.POST,instance=how)
        else: form=DealHowForm(request.POST)
        if form.is_valid():
            how_form=form.save(commit=False)
            how_form.save()
            messages.success(request, str(DEALS_MSG['HWS']))
            return HttpResponseRedirect(reverse('admin_portal_deals_how'))
        else:
            messages.error(request, str(DEALS_MSG['OOPS']))
            return HttpResponseRedirect(reverse('admin_portal_deals_how'))
    else:
        data = {'form':form,'how':how}
        return render_to_response (template, data, context_instance=RequestContext(request))    

@admin_required
def deals_how_delete(request):
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        fq = How.objects.filter(id__in=id)
        fq.delete()
        status=1
        msg=DEALS_MSG['HWD']
        mtype='s'
    except:
        status=0
        msg=DEALS_MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))   
  
