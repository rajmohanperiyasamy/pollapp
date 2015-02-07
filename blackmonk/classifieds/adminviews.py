from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from urllib import urlopen

from classifieds.forms import ClassifiedCategoryForm, ClassifiedCategorySeoForm, \
    ClassifiedAttributeForm, ClassifiedPricingForm, OodleSettingsForm
from classifieds.models import ClassifiedCategory, ClassifiedAttribute, \
    Classifieds, ClassifiedPrice, OodleSettings
from common.admin_utils import response_to_save_attribute, \
    response_to_save_settings, response_delete_attribute, save_emailsettings, \
    get_emailsettings, success_response_to_save_parent_category, error_response, \
    response_delete_category
from common.forms import ApprovalSettingForm, SEOForm
from common.getunique import getUniqueValue
from common.models import ModuleNames, ApprovalSettings
from common.static_msg import CLASSIFIEDS_MSG
from common.templatetags.ds_utils import get_msg_class_name
from usermgmt.decorators import admin_required


@admin_required
def classifieds_settings(request, template='admin/portal/classifieds/settings.html'):
    approval=oodle=None
    active=inactive=0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
    LIST={'F':0,'S':0,'B':0}
    
    payment_level = ClassifiedPrice.objects.filter(level_visibility=True)
    total_atr=ClassifiedAttribute.objects.all().count()
    classifieds_state = Classifieds.objects.values('listing_type','is_active','status').annotate(s_count=Count('status'),a_count=Count('is_active'),f_count=Count('listing_type'))
    
    for st in classifieds_state:
        STATE[st['status']]+=st['s_count']
        try:LIST[st['listing_type']]+=st['f_count']
        except:pass
        if st['is_active']:
            active+=st['a_count']
        else:
            inactive+=st['a_count']
    
    cat_type = list(ClassifiedCategory.objects.values_list('parent', flat=True))
    total = len(cat_type)
    parent_cat = cat_type.count(None)
    sub_cat = total - parent_cat
    
    data={
          'classifieds_count':active+inactive,
          'active_classifieds':active,
          'inactive_classifieds':inactive,
          
          'published_classifieds':STATE['P'],
          'pending_classifieds':STATE['N'],
          'drafted_classifieds':STATE['D'],
          'rejected_classifieds':STATE['R'],
          'blocked_classifieds':STATE['B'],
          'expired_classifieds':STATE['E'],
          
          'featured_classifieds':LIST['F'],
          'sponsored_classifieds':LIST['S'],
          'basic_classifieds':LIST['B'],
          
          'category':sub_cat+parent_cat,
          'parent_category':parent_cat,
          'sub_category':sub_cat,
          
          'payment_level':payment_level,
          'total_atr':total_atr
    }
    try:
        approval = ApprovalSettings.objects.get(name='classifieds')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:
        oodle = OodleSettings.objects.all()[0]
        oodel_form=OodleSettingsForm(instance=oodle)
    except:
        oodel_form=OodleSettingsForm()
    try:seo = ModuleNames.get_module_seo(name='classifieds')
    except:seo = ModuleNames(name='classifieds')
    if request.method=='POST':
        ############################################
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        seo_form = SEOForm(request.POST)
        ############################################
        save_Oodle = request.POST['save_Oodle']
        if save_Oodle == "on":
            oodel_form=OodleSettingsForm(request.POST)
            if oodel_form.is_valid():
                oodel_form.save()
        else:
            oodel_form=OodleSettingsForm(instance=oodle)
        ############################################
        if approval_form.is_valid() and seo_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='classifieds'
            approvals.modified_by=request.user
            approvals.save()
            ############################################
            save_emailsettings(request,'classifieds')
            ############################################
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'oodel_form':oodel_form,
                         'classifieds':True,'emailsettings':get_emailsettings('classifieds')}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/classifieds/include_settings.html',CLASSIFIEDS_MSG)
        else:
            
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'oodel_form':oodel_form,
                         'classifieds':True,'emailsettings':get_emailsettings('classifieds')}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/classifieds/include_settings.html',CLASSIFIEDS_MSG)
    extra_data = {'seo':seo,'approval_form':approval_form,'oodel_form':oodel_form,
                         'classifieds':True,'emailsettings':get_emailsettings('classifieds')}
    data.update(extra_data)
    return render_to_response (template, data, context_instance=RequestContext(request))
    
def validate_oodle_api(request):
    key = request.POST['api_key']
    radius = request.POST['radius']
    location = request.POST['location']
    region = request.POST['region']
    category = 'job'
    url = 'http://api.oodle.com/api/v2/listings?key=%s&radius=%s&location=%s&region=%s&category=%s&num=25'%(key, radius, location, region, category)
    xml = urlopen(url).read()
    if "<error>Invalid API key" in xml: return HttpResponse("Oops!!! Invalid API key") 
    #if "<error>Invalid category" in xml: return HttpResponse("Invalid category")
    if "<error>Invalid region" in xml: return HttpResponse("Oops!!! Invalid region")
    return HttpResponse("Valid")

################################################## CATEGORY   #########################################

@admin_required
def classifieds_category(request, template='admin/portal/classifieds/category.html'):
    classifieds=ClassifiedCategory.objects.filter(parent=None)
    data={'parentcategoryes':classifieds}
    data['pcatcount']=classifieds.count()
    try:data['msg']=CLASSIFIEDS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def classifieds_category_update(request,template='admin/portal/classifieds/update_category.html'):
    data={}
    data['pcatcount']=ClassifiedCategory.objects.filter(parent=None).count()
    category=None
    try:
        category = ClassifiedCategory.objects.get(id = request.REQUEST['id'])
        form=ClassifiedCategoryForm(instance=category)
    except:form=ClassifiedCategoryForm()
    if request.method=='POST':
        if category:form=ClassifiedCategoryForm(request.POST,instance=category)
        else: form=ClassifiedCategoryForm(request.POST)
        if form.is_valid():
            cat_form=form.save(commit=False)
            if not cat_form.slug:cat_form.slug=getUniqueValue(ClassifiedCategory,slugify(cat_form.slug))
            else:cat_form.slug=getUniqueValue(ClassifiedCategory,slugify(cat_form.name))
            cat_form.save()
            form=ClassifiedCategoryForm()
            data['form']=form
            data['cat']=category
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_classifieds_category_update'),'classified':True}
            if category: MSG = {'CUS':'Classifieds Category Updated Successfully.'}
            else: MSG = {'CUS':'Classifieds Category Added Successfully.'}
            return success_response_to_save_parent_category(append_data,data,template,MSG,cat_form.parent)
        else:
            data['form']=form
            data['cat']=category
            return error_response(data,template,CLASSIFIEDS_MSG)
    data['form']=form
    data['cat']=category
    return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def classifieds_category_delete(request):
    data=response_delete_category(request,ClassifiedCategory,CLASSIFIEDS_MSG)
    data['count']=ClassifiedCategory.objects.all().count()
    return HttpResponse(simplejson.dumps(data))
    
@admin_required
def classifieds_seo_category_update(request, template='admin/portal/classifieds/update_category_seo.html'):
    try:
        category = ClassifiedCategory.objects.get(id = request.REQUEST['id'])
        form=ClassifiedCategorySeoForm(instance=category)
    except:return HttpResponse('Oops !!!Category Type not found.')
    if request.method=='POST':
        form=ClassifiedCategorySeoForm(request.POST,instance=category)
        if form.is_valid():
            cat_form=form.save(commit=False)
            cat_form.slug=slugify(cat_form.slug)
            cat_form.save()
            data={'status':1,'msg':str(CLASSIFIEDS_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data = {'form':form,'seo':category}
            return error_response(data,template,CLASSIFIEDS_MSG)
    data = {'form':form,'seo':category}
    return render_to_response (template, data, context_instance=RequestContext(request))


"""
######################################################################################################################
######################################  Calssifieds  ATTRIBUTES  #####################################################
######################################################################################################################
"""

@admin_required
def classifieds_attribute(request):
    categoryall = ClassifiedCategory.objects.filter(parent__isnull=True)
    try:page = int(request.GET['page'])
    except:page = 1
    data = {'categoryall':categoryall}
    data['url'] = reverse('admin_portal_classifieds_attribute')
    try:data['msg']=CLASSIFIEDS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response('admin/portal/classifieds/attribute.html', data, context_instance=RequestContext(request))

@admin_required
def classifieds_attributes_load(request):
    try:
        id=int(request.POST['id'])
        category = ClassifiedCategory.objects.get(id=id)
        try:attrbutes=ClassifiedAttribute.objects.filter(category__id=id).order_by('type')
        except:attrbutes=None
        try:
            if category.parent:parentattrbutes=ClassifiedAttribute.objects.filter(category__id=category.parent.id).order_by('type')
            else:parentattrbutes=None 
        except:parentattrbutes=None 
        data = {'category':category,'attrbutes':attrbutes,'parentattrbutes':parentattrbutes}
        return render_to_response('admin/portal/classifieds/include_attribute.html', data, context_instance=RequestContext(request))
    except:
        return HttpResponse(str(CLASSIFIEDS_MSG['OOPS']))

@admin_required
def classifieds_attribute_update(request,template='admin/portal/classifieds/update_attribute.html'):
    try:
        attr=selected_cat=dvalues=None
        default_values=''
        try:
            attr = ClassifiedAttribute.objects.get(id=int(request.REQUEST['id']))
            form = ClassifiedAttributeForm(instance=attr)
        except:form=ClassifiedAttributeForm()
        try:selected_cat = ClassifiedCategory.objects.get(id=int(request.REQUEST['cid']))
        except:
            if not attr:return HttpResponse(str(CLASSIFIEDS_MSG['OOPS']))
            else:selected_cat=attr.category
        if request.method=='POST':
            if attr:form = ClassifiedAttributeForm(request.POST, instance=attr)
            else:form = ClassifiedAttributeForm(request.POST)
            if form.is_valid():
                attrs = form.save(commit=False)
                attrs.type=request.POST['type'] 
                attrs.category=selected_cat
                try:dvalues = request.POST['default_values'].split(',')
                except:dvalues = request.POST['default_values']
                if dvalues:
                    for id,dv in enumerate(dvalues):
                        dv = dv.strip()
                        if dv != '':
                            if id!=0:default_values+=":|"+dv
                            else:default_values=dv
                attrs.default_values=default_values     
                attrs.save()
                form=ClassifiedAttributeForm()
                data={'attribute':attr,'selected_cat':selected_cat,'form':form}
                append_data={'cat':attrs,'edit_url':reverse('admin_portal_classifieds_attribute_update')}
                if attr: MSG = {'AUS': 'Classifieds Attribute Updated Successfully.'}
                else: MSG = {'AUS': 'Classifieds Attribute Added Successfully.'}
                return response_to_save_attribute(request,append_data,data,template,MSG)
            else:
                data={'attribute':attr,'selected_cat':selected_cat,'form':form}
                return error_response(data,template,CLASSIFIEDS_MSG)
        data={'attribute':attr,'selected_cat':selected_cat,'form':form}
        return render_to_response(template, data, context_instance=RequestContext(request))
    except:HttpResponse(str(CLASSIFIEDS_MSG['OOPS']))
       

@admin_required
def classifieds_attribute_delete(request):
    data=response_delete_attribute(request,ClassifiedAttribute,CLASSIFIEDS_MSG)
    return HttpResponse(simplejson.dumps(data))


"""
#####################################################################################################################
##################################   Classifieds PRICING ############################################################
#####################################################################################################################
"""   
    
@admin_required
def classifieds_price(request,template='admin/portal/classifieds/pricing.html'):
    ''' method for updating classified pricing informations '''
    data={}
    ClassifiedPriceFormsets=modelformset_factory(ClassifiedPrice,extra=3,form=ClassifiedPricingForm,max_num=3)
    classified_price_forms=ClassifiedPriceFormsets() 
    if request.method == 'POST':
        classified_price_forms=ClassifiedPriceFormsets(request.POST)
        if classified_price_forms.is_valid():
            classified_price_forms.save()
            messages.success(request, str(CLASSIFIEDS_MSG['PUS'])) 
            return HttpResponseRedirect(reverse('admin_portal_classifieds_price'))
    data['classified_price_forms']=classified_price_forms
    try:data['msg'] =CLASSIFIEDS_MSG[request.GET['msg']]
    except:data['msg'] =False
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype']=False
    return render_to_response(template, data, context_instance=RequestContext(request)) 



@admin_required
def classifieds_sponsored_price(request):
    error=""
    try:
        categories=ClassifiedCategory.objects.filter(parent=None).order_by('name')
        for cat in categories:
            sp_price=float(request.POST['sp_price%d'%(cat.id)])
            if sp_price > 0.0:
                cat.sp_price=sp_price
            else:
                error = "Please Enter SP Price Greater Than Zero(0)"
            cat.sp_price
            cat.save()
        if error:
            data={'msg':str(error),'mtype':get_msg_class_name('e')}
            return HttpResponse(simplejson.dumps(data))
        data={'msg':str(CLASSIFIEDS_MSG['CPUS']),'mtype':get_msg_class_name('s')}
        return HttpResponse(simplejson.dumps(data))
    except:
        data={'msg':str(CLASSIFIEDS_MSG['OOPS']),'mtype':get_msg_class_name('e')}
        return HttpResponse(simplejson.dumps(data))
