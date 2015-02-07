#Python

#Django
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count

#Library
from common.static_msg import ATTRACTION_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category,response_to_save_settings
from common.templatetags.ds_utils import get_msg_class_name
from common.forms import SEOForm
from common.models import ModuleNames
from common.getunique import getUniqueValue
from usermgmt.decorators import admin_required

from attraction.models import AttractionCategory,Attraction
from attraction.forms import AttractionCategoryForm,AttractionCategorySeoForm

"""
#####################################################################################################################
#################################   ADMIN PORTAL ATTRACTION  ########################################################
#####################################################################################################################
"""
@admin_required
def attraction_settings(request, template='admin/portal/attraction/settings.html'):
    active=inactive=0
    
    attraction_category=AttractionCategory.objects.all().count()
    attraction_state = Attraction.objects.values('is_active').annotate(a_count=Count('is_active'))
    
    for st in attraction_state:
       if st['is_active']:
            active+=st['a_count']
       else:
            inactive+=st['a_count']
    
    data={
          'no_attraction':inactive+active,
          'no_active_attraction':active,
          'no_inactive_attraction':inactive,
          'attraction_category':attraction_category,
    }
            
    try:seo = ModuleNames.get_module_seo(name='attraction')
    except:seo = ModuleNames(name='attraction')        
    if request.method=='POST':
        seo_form = SEOForm(request.POST)
        if seo_form.is_valid(): 
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/attraction/include_settings.html',ATTRACTION_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/attraction/include_settings.html',ATTRACTION_MSG)

    data['seo'] = seo
    return render_to_response (template, data, context_instance=RequestContext(request))


################################################## CATEGORY #########################################

@admin_required
def attraction_category(request, template='admin/portal/attraction/category.html'):
    attraction=AttractionCategory.objects.all().order_by('name')
    data={'attraction':attraction}
    try:data['msg']=ATTRACTION_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def attraction_category_update(request,template='admin/portal/attraction/update_category.html'):
    data={}
    cat=None
    try:cat = AttractionCategory.objects.get(id=request.REQUEST['id'])
    except:form = AttractionCategoryForm()
    form = AttractionCategoryForm(instance=cat)
    if request.method=='POST':
        if cat:form = AttractionCategoryForm(request.POST,instance=cat)
        else:form = AttractionCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if not cat:category.created_by=category.modified_by=request.user
            else:category.modified_by=request.user
            if cat:getUniqueValue(AttractionCategory,slugify(category.slug),instance_pk=category.id)
            else:getUniqueValue(AttractionCategory,slugify(category.slug))
            category.save()   
            form=AttractionCategoryForm()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('admin_portal_attraction_category_update')}
            return success_response_to_save_category(append_data,data,template,ATTRACTION_MSG)
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,ATTRACTION_MSG)
    data = {'form':form,'cat':cat}
    return render_to_response(template,data,context_instance=RequestContext(request))
     
@admin_required
def attraction_category_delete(request):
    data=response_delete_category(request,AttractionCategory,ATTRACTION_MSG)
    return HttpResponse(simplejson.dumps(data))
    
@admin_required
def attraction_seo_category_update(request, template='admin/portal/attraction/update_category_seo.html'):
    try:seo = AttractionCategory.objects.get(id=int(request.REQUEST['id']))
    except:return HttpResponse("Oops!!! Attraction Category not found")
    form = AttractionCategorySeoForm(instance=seo)
    if request.method=='POST':
        form = AttractionCategorySeoForm(request.POST,instance=seo)
        if form.is_valid():
            seo=form.save(commit=False)
            seo.slug=getUniqueValue(AttractionCategory,slugify(seo.slug),instance_pk=seo.id)
            seo.modified_by=request.user
            seo.save()
            data={'status':1,'msg':str(ATTRACTION_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data={'seo':seo,'form':form}
            return error_response(data,template,ATTRACTION_MSG)
    data={'seo':seo,'form':form}
    return render_to_response (template, data, context_instance=RequestContext(request))


